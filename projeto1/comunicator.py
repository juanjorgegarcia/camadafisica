
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
        bytesSeremLidos = self.com.rx.getBufferLen()
            
        self.data = self.com.getData()
        msgType = self.com.getMsgType(self.data)

        self.reply(msgType)
            


    def waitForResponse(self):
        running = True
        if self.client:
            self.sendInfo(1)
        while running:
            self.receiveInfo()

    def reply(self, msgType):
        if msgType == 1:
            self.sendInfo(2)
        elif msgType == 2:
            self.sendInfo(3)
            time.sleep(0.5)
            self.sendInfo(4, "./jovicone.jpg")
        elif msgType == 3:
            # openToReceiveData()
            print("Im ready son")
        elif msgType == 4:
            if self.com.verifyFileIntegrity(self.data):  
                self.saveFile(self.com.cleanMsg(self.data))
                self.sendInfo(5)
            else:
                self.sendInfo(7)
        elif msgType == 5:
            self.sendInfo(7)
            self.quitt()
        elif msgType == 6:
            self.sendInfo(4, "./smile.png")
        elif msgType == 7:
            self.quitt()


    def saveFile(self, data):
        with open("./ImageRecebida.jpg","wb") as f:
            f.write(data)

    def quitt(self):
        self.com.disable()


