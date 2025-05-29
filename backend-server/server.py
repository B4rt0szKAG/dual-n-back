import datetime
import socket
import json
import uuid
from Classes.session import SessionToken
from Classes.user import User
from passwords_hashing import *
from peewee import IntegrityError


def handle_register(data: dict, client_socket):
    user_data = data

    username = user_data.get('username')
    name = user_data.get('name')
    lastname = user_data.get('lastname')
    email = user_data.get('email')
    password = user_data.get('password')

    try:
        ok, info = check_pass_strength(password)

        if not ok:
            raise ValueError(info)
        pass_hashed = hash_pass(password)

        new_user = User.create(
            username = username,
            name = name,
            lastname = lastname,
            email = email,
            password = pass_hashed
        )
        print("dodałem")

    except IntegrityError:
        response = {
            'status': 'error',
            'message': f"Użytkownik {username} już istnieje"
        }

    except ValueError as ve:
        response = {
            'status': 'error',
            'message': str(ve)
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': "Nieoczekiwany błąd: " + str(e)
        }
        #TODO templete metod albo dekorator
    else:
        response = {
            'status': 'ok',
            'user_id': new_user.id
        }
    client_socket.send(json.dumps(response).encode('utf-8'))


def handle_login(data: dict, client_socket):
    user_data = data
    username = user_data.get('username')
    password = user_data.get('password')

    try:
        user = User.get(User.username == username)

        if check_pass(password, user.password.encode()):
            token = str(uuid.uuid4())

            try:
                expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                SessionToken.create(token=token, user_name=username, expires_at=expires)

                response = {'status': 'ok', 'token': token}
                client_socket.send(json.dumps(response).encode('utf-8'))
                print("zalogowałem")

            except IntegrityError:
                print(f"Błąd: Token {token} już istnieje w bazie")
                raise Exception("Błąd zapisu tokena: Token już istnieje")

    except IntegrityError:
        response = {
            'status': 'error',
            'message': 'such a user does not exist'
        }
        client_socket.send(json.dumps(response).encode('utf-8'))





def run_server(host = '127.0.0.1', port = 12345):

    srv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    srv.bind((host,port))
    srv.listen(5)
    print("serwer nasłuchuje")

    while True:
        client_socket, addr = srv.accept()

        raw = client_socket.recv(4096)

        response_decoded = raw.decode('utf-8')
        response = json.loads(response_decoded)

        try:
            action, body = response.get('action'), response.get('body')

            if action == 'register':
                handle_register(body, client_socket)
            elif action == 'login':
                handle_login(body, client_socket)
            else:
                response = {
                    'status': 'error',
                    'message': f" action not known: {action} "

                }
                client_socket.send(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            response = {
                'status': 'error',
                'message':  'json decode error'
            }
            client_socket.send(json.dumps(response).encode('utf-8'))

        finally:
            client_socket.close()






        client_socket.close()

if __name__ == '__main__':
    run_server()
