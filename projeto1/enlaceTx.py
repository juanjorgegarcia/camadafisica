#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Carareto
# 17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading

# Class


class TX(object):
    """ This class implements methods to handle the transmission
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica = fisica
        self.buffer = bytes(bytearray())
        self.transLen = 0
        self.empty = True
        self.threadMutex = False
        self.threadStop = False
        self.packages = []

    def createHeader(self, msgType, imgSize, packageNum, numOfPackages, errorNumPackage):
        bytesSize = imgSize.to_bytes(2, byteorder = "big")
        msgType = msgType.to_bytes(1, byteorder = "big")

        errorNumPackage = errorNumPackage.to_bytes(1, byteorder = "big")
        packageNum = packageNum.to_bytes(2, byteorder = "big")
        numOfPackages = numOfPackages.to_bytes(2, byteorder = "big")


        supposedTime = (imgSize*10)/(self.fisica.baudrate)
        # print(f"Supposed transfer time: {round(supposedTime,4)}")
       
        header = msgType + bytesSize + packageNum + numOfPackages + errorNumPackage

        return header

    def createPayload(self, filename):

        if filename != "":
            with open(filename, "rb") as img:
                payload = img.read()
            
        else:
            payload = (11).to_bytes(2, byteorder='big')
        
        return payload


    def createEOP(self):
        eop = (1024).to_bytes(2, byteorder='big')
        return eop

    def createPackages(self, msgType, filename, errorNumPackage=0):
        self.packages = []
        payload = self.createPayload(filename)
        eop = self.createEOP()
        stuf = (00).to_bytes(2, byteorder='big')

        if eop in payload:
            # print(f"a imagem possui um eop: {len(payload)}")
            new_payload = payload.replace(eop,stuf+eop)
            # print(f"nova str {len(new_payload)}")
            print("Stuffing had to be done --------------------------------------------------------------------------------------------")
        else:
            new_payload = payload
            # print("Stuffing nao foi feito")

        dividedFile = [new_payload[i:i+128] for i in range(0,len(new_payload),128)]
        # print(f'Quantidade de pacotes: {len(dividedFile)}')
        for i in range(len(dividedFile)):
            payload=dividedFile[i]
            payloadLen = len(payload)
            # print(f"Indice do pacote: {i}")
            # print(f'Tamanho do pacote: {len(payload)}')

            header = self.createHeader(msgType, payloadLen, i, len(dividedFile), errorNumPackage)

            # self.package = header + new_payload + eop
            # overhead = len(self.package)/len(payload)
            # print(f"Tamanho do pacote: {len(self.package)} bytes")
            # print(f"Overhead de {overhead} ")
            # print(f"Throughput: {overhead*self.fisica.baudrate} ")
            self.packages.append(header + payload + eop)
        return self.packages

    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        beginTime = time.clock()
        while not self.threadStop:
            if(self.threadMutex):

                self.transLen = self.fisica.write(self.buffer)

                #print("O tamanho transmitido. IMpressao dentro do thread {}" .format(self.transLen))
                self.threadMutex = False
        afterTime = time.clock()
        # print(f"Tempo real de envio no tx: {afterTime - beginTime}")

    def threadStart(self):
        """ Starts TX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill TX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the TX thread to run

        This must be used when manipulating the tx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the TX thread (after suspended)
        """
        self.threadMutex = True

    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """

        self.transLen = 0
        self.buffer = data
        self.threadMutex = True

    def getBufferLen(self):
        """ Return the total size of bytes in the TX buffer
        """
        return(len(self.buffer))

    def getStatus(self):
        """ Return the last transmission size
        """
        #print("O tamanho transmitido. Impressao fora do thread {}" .format(self.transLen))
        return(self.transLen)

    def getIsBussy(self):
        """ Return true if a transmission is ongoing
        """
        return(self.threadMutex)

    def getPackageByNum(self, packageNum):
        """ Return the exactly package number
        """
        return self.packages[packageNum]