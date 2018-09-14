
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
        self.message = 0
    def startCom(self):
        # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
        self.com = enlace(self.serialName)
    
        # Ativa comunicacao
        self.com.enable()


    def mountFilePackages(self, msgType, errorNumPackage = 0 ,filename = ""):
        self.filePackages = self.com.makePackages(msgType, errorNumPackage, filename)
   
    def sendInfo(self, packageNum = 0):
        


        self.com.sendData(self.filePackages[packageNum])

        # alo = time.time()

        # print(f"Tamanho da imagem: {(txLen)} bytes")
        # print(f"Tempo suposto de envio: {com.supposedTime(txLen)} ms")

    def receiveInfo(self):
        # Faz a recepção dos dados
        print ("Recebendo dados .... ")
        

        self.data = self.com.getData()
        
        if self.data == "TIMEOUT":
            print("DEU TIMEOUT")
            if self.state == 4:
                self.sendInfo(self.state, "./jovicone.jpg")
            elif self.state != 0:
                self.sendInfo(self.state)
        else:
            msgType = self.com.getMsgType(self.data)

            # self.reply(msgType)
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

    # def reply(self, msgType):
    #     if msgType == 1:
    #         self.state = 2
    #         self.sendInfo(2)
    #     elif msgType == 2:
    #         self.sendInfo(3)
    #         time.sleep(0.5)
    #         self.state = 4
    #         self.sendInfo(4, "./smile.png")
    #     elif msgType == 3:
    #         self.state = 3
    #         print("Im ready son")
    #     elif msgType == 4:
    #         if self.com.verifyFileIntegrity(self.data):  
    #             self.saveFile(self.com.cleanMsg(self.data))
    #             self.state = 5
    #             self.sendInfo(5)
    #         else:
    #             self.state = 6
    #             self.sendInfo(6)
    #     elif msgType == 5:
    #         self.state = 7
    #         self.sendInfo(7)
    #         time.sleep(0.5)
    #         self.quitt()
    #     elif msgType == 6:
    #         self.state = 4
    #         self.sendInfo(4, "./smile.png")
    #     elif msgType == 7:
    #         self.state = 7
    #         self.quitt()

    def respond(self, msgType):
        if self.state == 0:
            if msgType == 1:
                self.mountFilePackage(2)
                self.state = 2
                self.sendInfo()
                return
        elif self.state == 1:
            if msgType == 2:
                self.mountFilePackage(3)
                self.sendInfo()
                time.sleep(0.5)
                self.mountFilePackage(4, filename = "./jovicone.jpg" )
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
                if self.com.verifyNumberOfPackage(self.data, self.receivedPackage):
                    if self.com.verifyFileIntegrity(self.data):  
                        self.receivedPackage = self.com.getPackageNumber(self.data)
                        # self.saveFile(self.com.cleanMsg(self.data))
                        self.mountFilePackage(5)
                        self.message += self.data
                        self.sendInfo()
                        return
                    else:
                        
                        self.mountFilePackage(6)
                        self.sendInfo()
                        return
                else:
                    self.mountFilePackage(8, errorNumPackage = self.com.getPackageNumber(self.data) )
                    self.sendInfo()

                    return
                    # self.state = 8        
        elif self.state == 4:
            
            if msgType == 5:
                self.currentPackage += 1
                if self.currentPackage == len(self.filePackages):
                    print('Todos os Pacotes Foram enviados!!')
                    self.mountFilePackage(msgType=7)
                    self.sendInfo()
                    self.state = 7
                    self.quitt()
                else:
                    self.sendInfo(packageNum = self.currentPackage)   
               

                # self.state = 7
                # self.sendInfo(7)
                # time.sleep(0.5)
                # self.quitt()
                return
            elif msgType == 8:

                self.currentPackage =  self.com.getPackageNumber(self.data)
                self.sendInfo(packageNum = self.currentPackage)   
            elif msgType == 6:
                self.sendInfo(packageNum= self.currentPackage)
                return
        elif self.state == 5:
            if msgType == 7:
                self.state = 7
                print(f'Foram recebidos {self.receivedPackage} pacotes')
                prinf(f'Tamanho total do payload: {len(self.message)}')
                self.quitt()
                return
        else:
            print("Error: Invalid State ", self.state)
            return
        
        print("Error: Message Type Not Expected")

    def setState(self, newState):
        print(f"State Changed: {self.state} to {newState}")
        self.state = newState

    def saveFile(self, data):
        with open("./ImageRecebida.jpg","wb") as f:
            f.write(data)

    def quitt(self):
        self.com.disable()
        self.running = False
    

    def verifyNumberOfPackage(self, data, packageNum):
        dataNum = self.com.getPackageNumber(data)
        if dataNum == packageNum:
            return True
        else:
            return False

