from wsgiref import simple_server

import falcon

from falconer.db.utils import get_scoped_session_factory
from falconer.middlewares import SessionMiddleware
from .resources.inventory import ActorResource, FilmResource

Session = get_scoped_session_factory()

api = application = falcon.API(middleware=[SessionMiddleware(Session)])

actor = ActorResource()
api.add_route('/actors/', actor)
api.add_route('/actors/{resource_id:int}', actor)

film = FilmResource()
api.add_route('/films/', film)
api.add_route('/films/{resource_id:int}', film)

staff = FilmResource()
api.add_route('/staffs/', staff)
api.add_route('/staffs/{resource_id:int}', staff)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
