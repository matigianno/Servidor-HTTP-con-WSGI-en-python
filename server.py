import json
from wsgiref.simple_server import make_server

tasks = {}
next_id = 1
HEDERS = [("Content-Type", "application/json")]

# "def" sirve para definir una funcion, en este caso la funcion es "app"
# que obtiene "environ" y "start_response" como parametros.
# environ tiene dentro todo lo que se pide al servidor.
def app(environ, start_response):
    #proximo id a utilizar
    global next_id

    info = environ['PATH_INFO']
    verb = environ['REQUEST_METHOD']
    #el 0 es para evitar errores en caso de que el contenido este basio
    length = int(environ.get('CONTENT_LENGTH',0))
    length_content = environ['wsgi.input'].read(length)

    parts = info.strip('/').split('/')
    size = len(parts)

    # chequeo de lo que trae environ y según eso se ejecuta una rama distinta
    match verb:
        case 'GET':

            #si hay un solo elemento en la url entonces no se busca ID
            if size == 1:
                body = json.dumps(list(tasks.values())).encode('utf-8')
                start_response('200 OK', HEDERS)
                return [body]

            #si hay un dos elemento en la url entonces se busca ID
            elif size == 2:
                task = tasks.get(int(parts[1]))
                if task is None:
                    start_response('404 Not Found', HEDERS)
                    return [b"Tarea no encontrada"]

                body = json.dumps(task).encode('utf-8')
                start_response('200 OK', HEDERS)
                return [body]

            #si no hay nada entonces se da error
            else:
                start_response('404 Not Found', HEDERS)
                return [b"Ruta no encontrada"]

        case 'POST':
            if size != 1:
                start_response('404 Not Found', HEDERS)
                return [b"Ruta no encontrada"]

            else:
                tasks[next_id] = json.loads(length_content.decode('utf-8'))
                body = json.dumps(tasks[next_id]).encode('utf-8')
                next_id + 1

                start_response('201 Created', HEDERS)
                return [body]


        case 'PATCH':

            if size == 2:

                task_id = int(parts[1])

                if tasks.get(task_id) is None:
                    start_response('404 Not Found', HEDERS)
                    return [b"Ruta no encuentrada"]
                else:
                    #se toma los datos enviados por el usuario y luego se cargan en "task" que al apuntar a "taskS" hace la actualizacion del mismo
                    task.update(json.loads(length_content.decode('utf-8')))
                    body = json.dumps(task).encode('utf-8')
                    start_response('200 OK', HEDERS)
                    return [body]
                
            else:
                start_response('404 Not Found', HEDERS)
                return [b"Ruta no encuentrada"]

            
        case 'DELETE':

            if size == 2:

                task_id = int(parts[1])


                if tasks.get(task_id) is None:
                    start_response('404 Not Found', HEDERS)
                    return [b"Ruta no encuentrada"]

                else:
                    #se toma los datos enviados por el usuario y luego se cargan en "task" que al apuntar a "taskS" hace la actualizacion del mismo
                    tasks.pop(task_id)
                    start_response('204 No Content', HEDERS)
                    return [b""]          

            else:
                start_response('404 Not Found', HEDERS)
                return [b"Ruta no encuentrada"]            

        case _:
            start_response('405 Method Not Allowed', HEDERS)
            return [b"Hola"]


with make_server("", 9292, app) as server:
    print("Listening on http://localhost:9292")
    # lee todas las peticiones que llegan y llama de nuevo a "app"
    server.serve_forever()