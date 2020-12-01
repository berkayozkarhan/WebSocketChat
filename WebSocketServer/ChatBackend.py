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








