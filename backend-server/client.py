import datetime
import socket
import json
from Exceptions.logOutExceptions import NoAuthFile, ErrorlogOut
from Exceptions.statsExceptions import SendingDataError
from pathlib import Path
from Classes.user import User
from Classes.statstics import Statistics
import os
import time


def register(user):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    message = {
        'action': 'register',
        'body': {
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


def logIn(username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    message = {
        'action': 'login',
        'body': {
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

            user_auth_file = f"auth_{username}.json"

            with open(user_auth_file, 'w') as f:
                json.dump({'token': token}, f, indent=2)

            print("zalogowałem")

            localStats = Path(f"localStats_{username}.json")
            print(f"Sprawdzam czy istnieje {localStats}")
            if localStats.exists():
                print("Plik istnieje - wysyłam lokalne statystyki...")
                sendingStatsFromLocalToServer(username, token)
            else:
                print("Brak lokalnych statystyk do wysłania")
        else:
            raise Exception("login error", response_json.get('message'))

    except json.JSONDecodeError:
        print("Błąd kodowania json   eeee")

    except Exception as e:
        print(f"błąd: {e}")

    finally:
        client_socket.close()


def logOut(username):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    authFile = Path(f"auth_{username}.json")

    if not authFile.exists():
        raise NoAuthFile()

    with open(authFile, 'r', encoding='utf-8') as file:
        data = json.load(file)

    message = {
        'action': 'logout',
        'body': {
            'username': username,
            'token': data['token']
        }
    }

    message_json = json.dumps(message)
    client_socket.send(message_json.encode('utf-8'))

    response = client_socket.recv(1024)
    response_decoded = response.decode('utf-8')

    try:
        response_json = json.loads(response_decoded)
        print(response_json['message'])
        if response_json.get('status') == 'ok':
            authFile.unlink()
            print("wylogowałem")
        else:
            raise ErrorlogOut()
    except json.JSONDecodeError:
        print("Błąd kodowania json   eeee")


    finally:
        client_socket.close()


def saveLocalStats(stats: Statistics,username):  # są tylko zapisywane gdy użytkownik nie jest zalogowany
    newStats = stats.to_dict()
    authFile = Path(f"auth_{username}.json")
    localStats = Path(f"localStats_{username}.json")
    if not authFile.exists():
        if not localStats.exists():
            with open(localStats,"w",encoding="utf-8") as file:
                statsArray = []
                json.dump(statsArray,file,ensure_ascii=False,indent=2)

        with open(localStats,"r",encoding="utf-8") as fileMod:
            statsList = json.load(fileMod)

        statsList.append(newStats)

        with open(localStats,"w",encoding="utf-8") as saveFile:
            json.dump(statsList,saveFile,ensure_ascii= False,indent=2)


def sendingStatsFromLocalToServer(username,token):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    localStatsPath = Path(f"localStats_{username}.json")
    with open(localStatsPath,"r",encoding='utf-8') as localStatsFile:
        localStats = json.load(localStatsFile)

    message = {
        'action': 'sendStatsFromLocal',
        'body': {
            'username': username,
            'token': token,
            'statistics': localStats
        }
    }

    message_json = json.dumps(message)
    client_socket.send(message_json.encode('utf-8'))

    response = client_socket.recv(1024)
    response_decoded = response.decode('utf-8')
    try:
        response_json = json.loads(response_decoded)
        print(response_json['message'],'awdawdawkidkawd')
        if response_json.get('status') == 'ok':
            print("dane wysałane")
            os.remove(localStatsPath)
        else:
            raise SendingDataError()
    except json.JSONDecodeError:

        print("Błąd kodowania json   eeee")
    finally:
        client_socket.close()





def sendStats(stats: Statistics,
              username):  # statystyki będą automatycznie wysyłane na serwer jeśli użytkownik jest zalogowany po zakończonej grze
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    authFile = Path(f"auth_{username}.json")

    if not authFile.exists():
        raise NoAuthFile()

    with open(authFile, 'r', encoding='utf-8') as file:
        data = json.load(file)

    newStats = stats.to_dict()
    message = {
        'action': 'sendStats',
        'body': {
            'username': username,
            'token': data['token'],
            'statistics': newStats
        }
    }

    message_json = json.dumps(message)
    client_socket.send(message_json.encode('utf-8'))

    response = client_socket.recv(1024)
    response_decoded = response.decode('utf-8')

    try:
        response_json = json.loads(response_decoded)
        print(response_json['message'],'awdawdawkidkawd')
        if response_json.get('status') == 'ok':
            print("dane wysałane")
        else:
            raise SendingDataError()
    except json.JSONDecodeError:

        print("Błąd kodowania json   eeee")


    finally:
        client_socket.close()

user = User(
    username="p2111",
    name="Maciek",
    lastname="Kowalski",
    email="maciek@example.com",
    password="ECT9Cllzu47gQOk!!"
)

#register(user)
from datetime import datetime
stats = Statistics(
    user_name = 'p2111',
    day = datetime.now(),
    type_of_game='xd',
    points_scored=15
)

#saveLocalStats(stats,"p2111")


# print(newstats)
#
logIn(user.username, user.password)
# time.sleep(10)
# try:
#     sendStats(stats,'p10')
# except SendingDataError:
#     print('jestsem jebanym debilem')



# time.sleep(30)

# try:
#     logOut(user.username)
# except NoAuthFile:
#     print('nie ma pliku auth')
#
# except ErrorlogOut:
#     print("wyjabało się wylogowanie")
