from Client import Client
from MyMessage import MyMessage as MyMsg
import json
import asyncio
import datetime


def showClients(clients):
    if(clients):
        print("Active Users:")
        for client, _ in clients.items():
            print("-->", clients[client])


def kayitEkle(client):
    pass





async def sayClientWelcome(websocket,name):
    welcomeMsg = "Welcome to chatroom, {}".format(name)
    connectionEstablishedMsg = MyMsg("welcome-message",
                                     "server",
                                     name,
                                     welcomeMsg,
                                     datetime.datetime.utcnow().isoformat() + "Z")
    connectionEstablishedMsg_JSON = json.loads(json.dumps(connectionEstablishedMsg.__dict__))
    await websocket.send("{}".format(connectionEstablishedMsg_JSON))


async def notify_usersInfo(clientsList,clientsNotificationList,_client):
    if clientsNotificationList:
        onlineClientsMsg = MyMsg("online-clients",
                             "server",
                             _client.username,
                             format(clientsNotificationList),  # çevrimiçi kullanıcılar koyulacak.
                             datetime.datetime.utcnow().isoformat() + "Z")
        onlineClientsMsg_JSON = json.loads(json.dumps(onlineClientsMsg.__dict__))
    for client, _ in clientsList.items():
        if client != _client:
            await client.send("{}".format(onlineClientsMsg_JSON))  # Online kullanıcılar bildiriliyor.

async def notify_usersNumber(clients,websocket):
    if (len(clients) != 0):  # Son bağlanan kullanıcıdan başka kullanıcı varsa
        notificationConnectedUsers = MyMsg("directed-message",
                                           "server",
                                           "everyone",
                                           'There are {} other users connected.'.format(len(clients) - 1),
                                           datetime.datetime.utcnow().isoformat() + "Z")
        notificationConnectedUsers_JSON = json.loads(json.dumps(notificationConnectedUsers.__dict__))

        await websocket.send(
            "{}".format(notificationConnectedUsers_JSON))  # Çevrimiçi kullanıcı yoksa mesaj olarak bildiriliyor.

async def notify_New_User(clientsList,_client):
    for client, _ in clientsList.items():
        notificationConnected = MyMsg("broadcast",
                      "server",
                      "everyone",
                      _client.username + ' has joined the chat',
                      datetime.datetime.utcnow().isoformat() + "Z")
        notificationConnected_JSON = json.loads(json.dumps(notificationConnected.__dict__))
        await client.send("{}".format(notificationConnected_JSON))
        #await client.send(name + ' has joined the chat')







""""
class ChatBackend:
    def __init__(self):
        self.clients = list()


def state_event():
    return json.dumps({"type":"state"},**STATE)

def users_event(clients):
    for client, _ in clients.items():
        print("Users event çalışıyor.")
        client.userID
        print("Users event bitti")

async def notify_state(clients):
        if clients:
            message = state_event()
            await asyncio.wait([user.send(message) for user in clients])

async def notify_users(clients):
    if clients:
        message = users_event(clients)
        await asyncio.wait([user.send(message) for user in clients])

async def register(websocket,clients):
        clients.add(websocket)
        await notify_state(clients)

async def counter(websocket,path):
    #register(websocket) sends user_event() to websocket
    #await register(websocket,clients)
     pass
"""



