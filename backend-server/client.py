import datetime
import socket
import json

from peewee import IntegrityError

from Classes.user import User
from Classes.session import SessionToken

def register(user):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    message = {
        'action': 'register',
        'body':{
            'username': user.username,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
            'password': user.password
        }
    }
    message_json = json.dumps(message)
    client_socket.send(message_json.encode('utf-8'))

    response = client_socket.recv(4096)

    response_decoded = response.decode('utf-8')

    try:
        response_json = json.loads(response_decoded)
        if response_json.get('status') == 'ok':
            print("Rejestracja zakończona pomyślnie")
        else:
            print("Rejestracja nie powiodła się:", response_json.get('message'))

    except json.JSONDecodeError:
        print("Błąd kodowania json")

    except Exception as e:
        print(f"błąd: {e}")

    finally:
        client_socket.close()

def login(username,password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    message = {
        'action': 'login',
        'body':{
            'username': username,
            'password': password
        }
    }
    message_json = json.dumps(message)

    client_socket.send(message_json.encode('utf-8'))

    response = client_socket.recv(1024)

    response_decoded = response.decode('utf-8')

    try:
        response_json = json.loads(response_decoded)
        if response_json.get('status') == 'ok':
            token = response_json.get('token')

            try:
                expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

                SessionToken.create(token=token,user_name = username,expires_at=expires)
            except IntegrityError:
                print(f"Błąd: Token {token} już istnieje w bazie")
                raise Exception("Błąd zapisu tokena: Token już istnieje")

        else:
            raise Exception("Błąd rejstracji")
        #TODO stworzyć własny exception
    except json.JSONDecodeError:
        print("Błąd kodowania json")

    except Exception as e:
        print(f"błąd: {e}")

    finally:
        client_socket.close()


user = User(
    username="maciekawdawd",
    name="Maciek",
    lastname="Kowalski",
    email="maciek@example.com",
    password="kajwndaw%%&&AWdKAWD1J"
)

register(user)