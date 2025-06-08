import datetime
import socket
import json
import uuid
from Classes.session import SessionToken
from Classes.user import User
from Classes.statstics import Statistics
from passwords_hashing import *
from peewee import IntegrityError
from Exceptions.loginExceptions import WrongPass, WrongLogin, TokenAlreadyExists
from Exceptions.logOutExceptions import TokenDoesntExistInDB
import threading


def handle_ping():
    message = {
        'action': 'PING'
    }
    msg_json = json.dumps(message).encode('utf-8')
    while (True):
        toRemoveArray = []
        for username, client in clientsArray:
            client.send(msg_json)
            client.settimeout(5.0)
            try:
                response = client.recv(4096)
                response_decoded = response.decode('utf-8')
                response_json = json.loads(response_decoded)

                if (response_json.get('status') == 'PONG'):
                    print("wszytko ok pingujemy się ")
                    expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                    session = SessionToken.get(SessionToken.user_name == username)
                    print(session.expires_at)
                    session.expires_at = expires
                    print(session.expires_at)
                    session.save()

                else:
                    print(f"coś jest nie tak {response_decoded.get('status')}")
                    toRemoveArray.append((username, client))
                    query = SessionToken.delete().where(SessionToken.user_name == username)
                    delete_query = query.execute()
                    print("usunięto wszytkie tokeny użytkownika ")



            except socket.timeout:
                print("Timeout - brak odpowiedzi od klienta w 3 sekundy")
                toRemoveArray.append((username, client))
                query = SessionToken.delete().where(SessionToken.user_name == username)
                delete_query = query.execute()
                print("usunięto wszytkie tokeny użytkownika ")
        with clients_lock:
            for username, client in toRemoveArray:
                client.close()
                clientsArray.remove((username, client))


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
            username=username,
            name=name,
            lastname=lastname,
            email=email,
            password=pass_hashed
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
        # TODO templete metod albo dekorator
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
        try:
            user = User.get(User.username == username)
        except User.DoesNotExist:
            raise WrongLogin()

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
                raise TokenAlreadyExists(token)
        else:
            raise WrongPass()
    except IntegrityError:
        sendResponse('error', 'unknown error', client_socket)


def handle_logout(data: dict, client_socket):
    user_data = data
    username = user_data.get('username')
    token = user_data.get('token')

    try:
        sessionData = SessionToken.get(SessionToken.user_name == username)

    except SessionToken.DoesNotExist:
        raise TokenDoesntExistInDB

    if token == sessionData.token:
        sessionData.delete_instance()
        sendResponse('ok', 'logged out correctly', client_socket)
    else:
        sendResponse('errorToken', 'invalid Token', client_socket)


def handle_sendStats(data: dict, client_socket):
    user_data = data
    username = user_data.get('username')
    token = user_data.get('token')
    stats_dict = user_data.get('statistics')
    print(token)
    try:
        sessionData = SessionToken.get(SessionToken.user_name == username)
        print(sessionData)
    except SessionToken.DoesNotExist:
        raise TokenDoesntExistInDB

    if token == sessionData.token:
        new_stat = Statistics.create(
            user_name=stats_dict['user_name'],
            day=datetime.datetime.fromisoformat(stats_dict['day']),
            type_of_game=stats_dict['type_of_game'],
            points_scored=stats_dict['points_scored']
        )

        print('dodałem dane do bazy')
        sendResponse('ok', 'Data added to DB', client_socket)
    else:
        sendResponse('errorToken', 'invalid Token', client_socket)


def handle_sendStats_fromLocal(data: dict, client_socket):
    user_data = data
    username = user_data.get('username')
    token = user_data.get('token')
    stats_dict = user_data.get('statistics')
    print(token)
    try:
        sessionData = SessionToken.get(SessionToken.user_name == username)
        print(sessionData)
    except SessionToken.DoesNotExist:
        raise TokenDoesntExistInDB

    if token == sessionData.token:

        for el in stats_dict:
            new_stat = Statistics.create(
                user_name=el['user_name'],
                day=datetime.datetime.fromisoformat(el['day']),
                type_of_game=el['type_of_game'],
                points_scored=el['points_scored']
            )

        print('dodałem dane do bazy')
        sendResponse('ok', 'Data added to DB', client_socket)
    else:
        sendResponse('errorToken', 'invalid Token', client_socket)


def sendResponse(status, message, client_socket):
    response = {
        'status': status,
        'message': message
    }
    client_socket.send(json.dumps(response).encode('utf-8'))
    client_socket.close()


clientsArray = []
clients_lock = threading.Lock()


def run_server(host='127.0.0.1', port=12345):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((host, port))
    srv.settimeout(1.0)
    srv.listen(5)
    print("serwer nasłuchuje")

    try:
        while True:
            try:
                client_socket, addr = srv.accept()
            except socket.timeout:
                continue
            raw = client_socket.recv(4096)

            response_decoded = raw.decode('utf-8')
            response = json.loads(response_decoded)

            try:
                action, body = response.get('action'), response.get('body')

                if action == 'register':
                    handle_register(body, client_socket)
                elif action == 'login':
                    handle_login(body, client_socket)
                elif action == 'logout':
                    handle_logout(body, client_socket)
                elif action == 'sendStats':
                    handle_sendStats(body, client_socket)
                elif action == 'sendStatsFromLocal':
                    handle_sendStats_fromLocal(body, client_socket)
                elif action == 'FirstPing':
                    with clients_lock:
                        clientsArray.append((body.get('username'), client_socket))
                else:
                    sendResponse('error', f" action not known: {action} ", client_socket)
            except TokenAlreadyExists as e:
                sendResponse('tokenError', f"such a token {e.token} already exists", client_socket)
            except WrongLogin:
                sendResponse('errorLogin', 'login incorrect', client_socket)
            except WrongPass:
                sendResponse('errorPassword', 'password incorrect', client_socket)
            except json.JSONDecodeError:
                sendResponse('error', 'json decode error', client_socket)
            except TokenDoesntExistInDB:
                sendResponse('error', 'Token doesnt exists in DB', client_socket)
    except KeyboardInterrupt:
        print("Zatrzymywanie serwera...")

    finally:
        srv.close()


if __name__ == '__main__':
    ping_thread = threading.Thread(target=handle_ping, daemon=True)
    ping_thread.start()
    run_server()
