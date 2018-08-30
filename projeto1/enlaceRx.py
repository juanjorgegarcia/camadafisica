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
        # h = self.buffer[0:2]
        b = self.buffer[0:nData]
        # eop = self.buffer[nData:]

        # h = int.from_bytes(h, byteorder= "big")
        # if (h != len(b)):
        #     print(f"Deu errado! Tamanho: {len(b)}")
        # else:
        # print(f"Deu certo! Tamanho {len(b)}")

        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """

        running = True


        eop = (1024).to_bytes(2, byteorder='big')   

        dataSize = 0


        stuf = (00).to_bytes(2, byteorder='big')
        stuffedEOP = 0
        realEOP = 0
        bufferLido = b''
        sleepTime = .5
        counter = 0
        receivingTime = time.time()
        while running:
            bufferLen = self.getBufferLen()
            bufferLido += self.getBuffer(bufferLen)
            time.sleep(.5)
            print(len(bufferLido))
            if eop in bufferLido:
                stuffedEOP = bufferLido.count(stuf+eop)
                realEOP = bufferLido.count(eop)

            if bufferLen == 0 and len(bufferLido) != 0:
                counter += 1
            else:
                counter = 0
            
            # print(f"StufferEOP: {stuffedEOP}")
            # print(f"realEOP: {realEOP}")
            if realEOP > stuffedEOP:
                print("Mensagem acabou")
                break
            elif counter > 4:
                print("Timeout: eop nao localizado")
                break
            
        eopIndex = bufferLido.rindex(eop)
        print(f"Posição do EOP {eopIndex}")
        msg = bufferLido.replace(stuf+eop,eop)
        # stopTime = time.time()
        # print(f"Tempo para recebimento da imagen: {stopTime-receivingTime} s")
        return(msg)

    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""

    def verifyFileIntegrity(self, msg):
        if len(self.getPayload(msg)) != int.from_bytes(msg[1:3], byteorder = "big"):
            print("Erro no numero de bytes recebidos")
            return False
        else:
            print("Mensagem recebida com sucesso")
            return True

    def verifyMsgType(self, msg):
        msgType = int.from_bytes(msg[0], byteorder = "big")
        print(f"Received message of Type {msgType}")

        return (msgType)

    def getPayload(self, msg):
        eop = (1024).to_bytes(2, byteorder='big')
        payload = msg[3:(len(msg)-len(eop))]
        return payload