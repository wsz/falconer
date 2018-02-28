class SessionMiddleware:
    def __init__(self, session):
        self.session = session

    def process_resource(self, req, resp, resource, params):
        resource.session = self.session()

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'session'):
            if req_succeeded:
                resource.session.commit()
            else:
                resource.session.rollback()
            self.session.remove()
