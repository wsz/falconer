from falcon import HTTPBadRequest


class HTTPInvalidParams(HTTPBadRequest):
    def __init__(self, msg, param_name, **kwargs):
        super()
