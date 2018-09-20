
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# JJ e Guigui
# 30/08/2018
#  Comunicador
####################################################

from enlace import *
import time


class Comunicator():
    def __init__(self, serialName, client):
        self.serialName = serialName
        self.com = None
        self.client = True if client == "-c" else False
        self.filePackages = []
        self.currentPackage = 0
        self.receivedPackage = 0
        self.message = None
    def startCom(self):
        # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
        self.com = enlace(self.serialName)
    
        # Ativa comunicacao
        self.com.enable()


    def mountFilePackages(self, msgType, errorNumPackage = 0 ,filename = ""):
        self.currentPackage = 0
        self.filePackages = self.com.makePackages(msgType,filename, errorNumPackage)
        
        # print(f"MOUNT FILE OF TYPE {self.com.getMsgType(self.filePackages[0])}")

   
    def sendInfo(self, packageNum = 0):
        print(f"Sending Data: type {self.com.getMsgType(self.filePackages[packageNum])} / PackNum:total {packageNum}:{len(self.filePackages)} / Pack size {len(self.filePackages[packageNum])} / Payload size {len(self.com.getPayload(self.filePackages[packageNum]))} / Type8 addon {int.from_bytes(self.filePackages[packageNum][7:8], byteorder = 'big')}")
        self.com.sendData(self.filePackages[packageNum])

        # alo = time.time()

        # print(f"Tamanho da imagem: {(txLen)} bytes")
        # print(f"Tempo suposto de envio: {com.supposedTime(txLen)} ms")

    def receiveInfo(self):
        # Faz a recepção dos dados
        print("Receiving ...")
        

        self.data = self.com.getData()
        
        if self.data == "TIMEOUT":
            print("DEU TIMEOUT")
            if self.state == 4:
                self.sendInfo(self.currentPackage)
            elif self.state == 3:
                self.mountFilePackages(8, errorNumPackage = self.receivedPackage -1)
                self.sendInfo()
            elif self.state != 0:
                self.mountFilePackages(self.state)
                self.sendInfo()
        else:
            msgType = self.com.getMsgType(self.data)
            
            self.respond(msgType)


    def waitForResponse(self):
        self.running = True
        self.state = 0
        if self.client:
            self.mountFilePackages(1)
            self.state = 1
            self.sendInfo()
        while self.running:
            self.receiveInfo()


    def respond(self, msgType):
        print(f"Received message: type {msgType} / PackNum:total {self.com.getPackageNumber(self.data)}:{self.com.getNumberOfPackages(self.data)}")
        if self.state == 0:
            if msgType == 1:
                self.mountFilePackages(2)
                self.state = 2
                self.sendInfo()
                return
        elif self.state == 1:
            if msgType == 2:
                self.mountFilePackages(3)
                self.sendInfo()
                time.sleep(0.5)
                self.mountFilePackages(4, filename = "./smalljoji.jpg" )
                self.state = 4
                self.sendInfo(self.currentPackage)
                return
        elif self.state == 2:
            if msgType == 3:
                self.state = 3
                print("Im ready son")
                return
        elif self.state == 3:
            if msgType == 4:
                if self.verifyNumberOfPackage(self.data, self.receivedPackage):
                    if self.com.verifyFileIntegrity(self.data): 
                        if self.CRCTest16(self.data): 
                            self.receivedPackage += 1
                            self.mountFilePackages(5)
                            if (self.message == None):
                                self.message = bytearray(self.com.getPayload(self.data))
                            else:
                                self.message += (bytearray(self.com.getPayload(self.data)))
                            self.sendInfo()
                            return
                        else:
                            print(f'Failed to pass CRC test')
                            self.mountFilePackages(6)
                            self.sendInfo()
                            return
                    else:
                        print(f'Payload size incorrect')
                        self.mountFilePackages(6)
                        self.sendInfo()
                        return
                else:
                    print(f"Received wrong Package: wanted No.{self.receivedPackage} / received No.{self.com.getPackageNumber(self.data)}")
                    self.mountFilePackages(8, errorNumPackage = self.receivedPackage)
                    self.sendInfo()

                    return
            elif msgType == 7:
                self.saveFile(self.message)
                print("Message Saved!")
                print(f'{self.receivedPackage} Packages received')
                print(f'File size: {len(self.message)} bytes')
                self.quitt()
                return

        elif self.state == 4:
            
            if msgType == 5:
                self.currentPackage += 1
                if self.currentPackage == len(self.filePackages):
                    print('All packages were sent!!')
                    self.mountFilePackages(msgType=7)
                    self.sendInfo()
                    self.state = 7
                    self.quitt()
                else:
                    self.sendInfo(packageNum = self.currentPackage)   
                return

            elif msgType == 8:
                self.currentPackage = self.com.getType8Addon(self.data)
                self.sendInfo(packageNum = self.currentPackage) 
                return 

            elif msgType == 6:
                self.sendInfo(packageNum=self.currentPackage)
                return
        else:
            print("Error: Invalid State ", self.state)
            return
        
        print("Error: Message Type Not Expected")

    def setState(self, newState):
        print(f"State Changed: {self.state} to {newState}")
        self.state = newState

    def saveFile(self, data):
        noStufData = self.com.cleanStuffing(data)
        print("Stuff cleaned")
        with open("./ImageRecebida.jpg","wb") as f:
            f.write(noStufData)

    def quitt(self):
        self.com.disable()
        self.running = False
    

    def verifyNumberOfPackage(self, data, packageNum):
        dataNum = self.com.getPackageNumber(data)
        if dataNum == packageNum:
            return True
        else:
            return False

    def CRCTest16(self, data):
        payload = self.com.getPayload(data)
        intPayload = int.from_bytes(payload, byteorder="big")

        bits = self.com.crc16(intPayload)

        if self.com.getCRCResult(data) == bits:
            return True
        else:
            return False