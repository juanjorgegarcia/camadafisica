
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

    def startCom(self):
        # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
        self.com = enlace(self.serialName)
    
        # Ativa comunicacao
        self.com.enable()

    def sendInfo(self, msgType, fileName=""):
        
        print(f"Transfering data of Type {msgType} ...")

        package = self.com.makePackage(msgType, fileName)

        # Transmite dado
        self.com.sendData(package)

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
            self.state = 1
            self.sendInfo(1)
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
                self.state = 2
                self.sendInfo(2)
                return
        elif self.state == 1:
            if msgType == 2:
                self.sendInfo(3)
                time.sleep(0.5)
                self.state = 4
                self.sendInfo(4, "./jovicone.jpg")
                return
        elif self.state == 2:
            if msgType == 3:
                self.state = 3
                print("Im ready son")
                return
        elif self.state == 3:
            if msgType == 4:
                if self.com.verifyFileIntegrity(self.data):  
                    self.saveFile(self.com.cleanMsg(self.data))
                    self.state = 5
                    self.sendInfo(5)
                    return
                else:
                    self.state = 6
                    self.sendInfo(6)
                    return
        elif self.state == 4:
            if msgType == 5:
                self.state = 7
                self.sendInfo(7)
                time.sleep(0.5)
                self.quitt()
                return
            elif msgType == 6:
                self.sendInfo(4, "./jovicone.jpg")
                return
        elif self.state == 5:
            if msgType == 7:
                self.state = 7
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
        


