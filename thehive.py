import requests
from urllib.parse import urljoin

class ThehiveClient(requests.Session):

    def __init__(self, remote, key, verify=True):
        """Authenticate a session with remote."""
        super().__init__()
        self.remote = remote
        self.headers['Authorization'] = f'Bearer {key}'
        self.verify = verify

    def request(self, method, url, *args, **kwargs):
        complete_url = urljoin(self.remote, url)
        return super().request(method, complete_url, *args, **kwargs)

    @classmethod
    def get_case_link(self, case_id, remote):
        """Return a link to access the case in the WebUI."""
        return urljoin(remote or self.remote, f'cases/{case_id}/details')

    @classmethod
    def get_task_link(self, task_id, case_id, remote):
        """Return a link to access the task from WebUI."""
        return urljoin(remote, f'cases/{case_id}/tasks/{task_id}')

    def get_tasks(self, open=None):
        data={
            "query": [
                {
                    "_name": "listTask"
                },
            ]
        }
        if open:
            data['query'].append(
                {
                    "_name": "filter",
                    "_eq": {
                        "_field": "status",
                        "_value": "Waiting"
                    }
                }
            )
        r = self.post('/api/v1/query', json=data)
        r.raise_for_status()
        return r.json()

    def get_cases(self, open=None):
        """Return the list of the cases."""
        data={
            "query": [
                {
                    "_name": "listCase"
                },
            ]
        }
        if open:
            data['query'].append(
                {
                    "_name": "filter",
                    "_in": {
                        "_field": "status",
                        "_values": ["New", "InProgress"]
                    }
                }
            )
        r = self.post('/api/v1/query', json=data)
        r.raise_for_status()
        return r.json()
