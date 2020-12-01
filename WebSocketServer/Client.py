
from GenerateID import GenerateUniqueID
import json
class Client:
    def __init__(self,username,userID,status,connected):
        self.username = username
        self.userID = userID
        self.status = status
        self.connected = connected
        #self.relatedSocket = relatedSocket
    def showInfo(self):
        print("Username :",self.username)
        print("User ID :",self.userID)
        print("Status: ",self.status)
        print("Connected :",self.connected)
        #print("Related Socket :",self.relatedSocket)

