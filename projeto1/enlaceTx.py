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


    def createHeader(self, imgSize):
        bytesSize = imgSize.to_bytes(2, byteorder = "big")
        return bytesSize

    def createPayload(self, filename):
        with open(filename, "rb") as img:
            payload = img.read()

        payload = b'ronaldo' +payload
        return payload

    def createEOP(self):
        eop = b'ronaldo'

        return eop

    def createPackage(self, filename):
        payload = self.createPayload(filename)
        eop = self.createEOP()
        stuf = b'00'
        if eop in payload:
            print(f"a imagem possui um eop: {payload}")
            new_payload = payload.replace(eop,stuf+eop)
            print(f"nova str {new_payload}")

        payloadLen = len(payload)
        print("tentado transmitir .... {} bytes".format(len(new_payload)))

        header = self.createHeader(payloadLen)
        

        self.package = header+new_payload+eop
        print(f"Esse é o pacote {self.package}")
        return self.package

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
