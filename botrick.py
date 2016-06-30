from wsgiref.simple_server import make_server
from markov import Markov
from pyramid.config import Configurator
from pyramid.response import Response

markov = Markov()


def get_botrick(request):
    return Response(markov.generate_text(500))


if __name__ == '__main__':
    config = Configurator()
    config.add_route('patrick', '/patrick')
    config.add_view(get_botrick, route_name='patrick')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()

