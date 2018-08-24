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


class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica = fisica
        self.buffer = bytes(bytearray())
        self.threadStop = False
        self.threadMutex = True
        self.READLEN = 1024

    def thread(self):
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado. 
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.01)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        h = self.buffer[0:2]
        b = self.buffer[2:nData]
        # eop = self.buffer[nData:]

        h = int.from_bytes(h, byteorder= "big")
        if (h != len(b)):
            print(f"Deu errado! Tamanho: {len(b)}")
        else:
            print(f"Deu certo! Tamanho {len(b)}")

        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )

        # if self.getBufferLen() < size:
        #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))

        # while(self.getBufferLen() < size):
        #     time.sleep(0.05)
#
#         running = True

        dataSize = 0

        receivingTime = 0
        while (self.getBufferLen() > dataSize) or (self.getBufferLen() == 0):
            if self.getBufferLen() != 0:
                receivingTime = time.time()
            dataSize = self.getBufferLen()
            
            time.sleep(1.50)
            print(f"BufferLen: {self.getBufferLen()}")
        stopTime = time.time()
        print(f"Tempo para recebimento da imagen: {stopTime-receivingTime}")
        return(self.getBuffer(dataSize))

    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
