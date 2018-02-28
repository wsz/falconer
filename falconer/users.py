import json

import falcon


class Resource:
    def on_get(self, req, resp):
        users = {
            'users': [
                {
                    'name': 'Admin',
                    'email': 'admin@example.com'
                }
            ]
        }

        resp.body = json.dumps(users, ensure_ascii=False)

        resp.status = falcon.HTTP_200
