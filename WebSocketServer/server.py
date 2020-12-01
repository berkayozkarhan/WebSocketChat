import asyncio
import json
from Client import Client
from ChatBackend import *
from GenerateID import GenerateUniqueID
from MyMessage import MyMessage as MyMsg
import datetime


#Mesajları her zaman oluşturduğum MyMessage classını referans alarak gönder.
#Çünkü C# tarafında da aynı niteliklere sahip class var.aksi halde json parse işleminde sıkıntı oluyor.
#-Berkay


#Sunucuya bağlanan istemcilerin listesi.Birisi server tarafında mesaj yönlendirme işlemi için diğeri de sunucuya bağlanan
#istemciye çevrimiçi kullanıcıları bildirmek için.Server tarafındaki liste websocket nesnesini içeriyor.
clients = {} #:(websocket:name)
clientsNotification = [] #istemciye gönderilecek liste
@asyncio.coroutine
async def client_handler(websocket,path):

    print("New Client ",websocket)
    print('({} existing clients)'.format(len(clients)))
    #İstemciden gelen ilk data ismi olarak belirlendi.
    first_data = await websocket.recv() #ilk mesajın geleceği yer istemcideki FirstMessage sınıfı
    first_data_json = json.loads(first_data)
    name = first_data_json['user_name']  # Hoşgeldin demek için isim seçiliyor.
    await sayClientWelcome(websocket,name)

    _client = Client(name,"{}".format(GenerateUniqueID()), "online", True)
    kayitEkle(_client)#bu fonksiyonda oluşturulan client nesnesi users veritabanına eklenmeli.
    #clients listesi server tarafında yönlendirme yapmak amacıyla oluşturuldu.clientsNotification ise istemciye online
    #kullanıcıları bildirmek üzere oluşturuldu.Aralarındaki temel fark clients listesinin websocket verisini içermesidir.
    #Çünkü sefver tarafında yönlendirme yapmak için websocket.send() fonksiyonu gereklidir ve bunun için de ilgili
    #soket nesnesinin bulunması gerekir.İstemciden gelen mesajlar yönlendirilirken user_ID değerine göre soket nesnesi
    #seçilip yönlendirilecektir.-Berkay
    clients[websocket] = {"name": name,"user_id":_client.userID} 
    clientsNotification.append({"username":name,"user_ID":"{}".format(_client.userID),"status":_client.status})
    print("--------------------------------------------")
    print('({} existing clients)'.format(len(clients)))
    _client.showInfo()  # Dahil olan istemcinin bilgileri yazdırılıyor.
    print("--------------------------------------------")
    await notify_usersInfo(clients,clientsNotification,_client)#Odada bulunan kullanıcıların isim ve id bilgileri.
    await notify_usersNumber(clients,websocket)#Odada bulunan kullanıcıların sayısı(Keyfi bir bildirim,olmasa da olur.)
    print ("Connection added:{}".format(clients[websocket]))
    print("--------------------------------------------")
    showClients(clients)
    print("--------------------------------------------")
    await notify_New_User(clients,_client)

    #Handle messages from this client
    while True:
        incoming_data = await websocket.recv()#Mesajlaşmanın başladığı yer.
        incoming_data_json = json.loads(incoming_data)#C#'tan gelen Message sınıfı parçalanıyor.
        print("incoming_data_json:")
        print(incoming_data_json)#Json pars edilen data kontrol amaçlı ekrana yazılıyor.
        message = incoming_data_json['message']#Gelen veriden mesaj bilgisi ayrılıyor.
        #Bu noktada gelen mesajın türüne göre yönlendirme işlemi yapılacak.Aynı zamanda .net tarafında disconnect butonuna basıldığında gönderilecek sunucudan ayrılma isteği ile
        #ilgili istemci çevrimiçi listesinden çıkarılacak.
        # Herhangi bir istemci mesaj gönderdiği zaman.Aynı zamanda mesaj yönlendirme işlemi buraya eklenecek.
        for client, _ in clients.items():
            if client != _client:#Mesajı gönderen istemciye tekrar mesajı göndermemek için liste içinde kontrol ediliyor.
                messageToAllUsers = MyMsg("broadcast",
                                                   "server",
                                                   "everyone",
                                                   "{}: {}".format(_client.username, message),
                                                   datetime.datetime.utcnow().isoformat() + "Z")
                messageToAllUsers_JSON = json.loads(json.dumps(messageToAllUsers.__dict__))
                await client.send("{}".format(messageToAllUsers_JSON))
                

        if message is None:
            their_name = clients[websocket]
            del clients[websocket]
            print('Client closed connection:',websocket)
            for client, _ in clients.items():
                await client.send(their_name +'has left the chat')
            break

            #Send message to all clients
            #for client, _ in clients.items():
                #await client.send("{}: {}".format(name,message))





