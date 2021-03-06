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

# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX


class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica = fisica(name)
        self.rx = RX(self.fisica)
        self.tx = TX(self.fisica)
        self.connected = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        self.tx.sendBuffer(data)

    def makePackages(self, msgType, filename, errorNumPackage):
        package = self.tx.createPackages(msgType, filename,errorNumPackage)
        return package

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        data = self.rx.getNData()

        return (data)

    def supposedTime(self, filesize):
        time = (filesize*11*1024)/(self.fisica.baudrate)
        return time
    
    def receiveData(self):
        return self.rx.receivedData

    def getMsgType(self, data):
        return (self.rx.verifyMsgType(data))

    def verifyFileIntegrity(self, data):
        return self.rx.verifyFileIntegrity(data)

    def getPackageNumber(self,data):
        return self.rx.getPackageNumber(data)

    def getNumberOfPackages(self, data):
        total = self.rx.getNumberOfPackages(data)
        return total

    def getPackageByNum(self, packageNum):
        return self.tx.getPackageByNum(packageNum)

    def getPayload(self, data):
        return self.rx.getPayload(data)

    def cleanStuffing(self, data):
        return self.rx.cleanStuffing(data)

    def getType8Addon(self, data):
        addon = self.rx.getType8Addon(data)
        return addon

    def crc16(self, data):
        return self.tx.crc16(data)

    def getCRCResult(self, data):
        return self.rx.getCRCResult(data)