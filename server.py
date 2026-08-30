from wsgiref.simple_server import make_server
import json

tasks ={}

next_id = 1

# seccion encargada de obtener los dats de entrada y trabajar con ellos
def app(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    # seccion encargada de leer cuantos segmentos tiene la url que se encuentra luego del verbo
    # para luego trabajar con ello
    match method:
        case ("GET", 1):
            body = json.dumps(list(tasks.values())).encode('utf-8')
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [body]

        case ("POST", 1):
            ...
        case ("PATCH", 1):
            ...
        case ("DELETE",1 ):
            ...

if __name__ == '__main__':
    server = make_server('localhost', 9292, app)
    server.serve_forever()