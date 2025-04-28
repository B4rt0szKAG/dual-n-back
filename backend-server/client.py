import socket
import json
from Classes.user import User

def register(user):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    user_data = {
        'username': user.username,
        'name': user.name,
        'lastname': user.lastname,
        'email': user.email,
        'password': user.password
    }

    request = {
        'user' : user_data
    }

    body = json.dumps(request)

    header = f"action:register_user\n"

    message = header + body

    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(4096)

    response_decoded = response.decode('utf-8')

    try:
        response_json = json.loads(response_decoded)
        if response_json.get('status') == 'ok':
            print("Rejestracja zakończona pomyślnie")
        else:
            # wypisz dokładny powód
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

    request = {
        'username': username,
        'password': password
    }

    body = json.dumps(request)

    header = f"action:login_user\n"

    message = header + body

    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(1024)

    response_decoded = response.decode('utf-8')

    try:
        response_json = json.loads(response_decoded)
        if response_json.get('status') == 'ok':
            token = response_json.get('token')
            return token
        else:
            raise Exception("Błąd rejstracji")
    except json.JSONDecodeError:
        print("Błąd kodowania json")

    except Exception as e:
        print(f"błąd: {e}")

    finally:
        client_socket.close()


user = User(
    username="pawel123",
    name="Paweł",
    lastname="Kowalski",
    email="pawel@example.com",
    password="AWD22q4nsef%#kkawd"
)

register(user)