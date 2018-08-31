#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################################
#Carareto
#17/02/2018
####################################################

# Importa pacote de comunicação serial
import serial

# importa pacote para conversão binário ascii
import binascii
import time
#################################
# Interface com a camada física #
#################################
class fisica(object):
    """ This class implements methods to handler the uart communication
    """
    def __init__(self, name):
        self.name        = name
        self.port        = None
        self.baudrate    = 115200
        #self.baudrate    = 9600
        self.bytesize    = serial.EIGHTBITS
        self.parity      = serial.PARITY_NONE
        self.stop        = serial.STOPBITS_ONE
        self.timeout     = 0.5
        self.rxRemain    = b""

        self.temporeal = 0

    def open(self):
        """ Opens serial port and configure it
        """
        self.port = serial.Serial(self.name,
                                  self.baudrate,
                                  self.bytesize,
                                  self.parity,
                                  self.stop,
                                  self.timeout)


    def close(self):
        """ Close serial port
        """
        self.port.close()

    def flush(self):
        """ Clear serial data
        """
        beginTime = time.clock()
        self.port.flushInput()
        self.port.flushOutput()
        afterTime= time.clock()
        global temporeal
        self.temporeal = alo-oi
        print(f"Tempo real de envio dentro do flus: {afterTime - beginTime} s")
        print("ALGUMA COISA TEM Q PRINTAR")

    def encode(self, data):
        """ Encode TX as ASCII data for transmission
        """
        encoded = binascii.hexlify(data)
        return(encoded)

    def decode(self, data):
        """ Decode RX ASCII data after reception
        """
        decoded = binascii.unhexlify(data)
        return(decoded)

    def write(self, txBuffer):
        """ Write data to serial port

        This command takes a buffer and format
        it before transmit. This is necessary
        because the pyserial and arduino uses
        Software flow control between both
        sides of communication.
        """
        startTime = time.time()
        nTx = self.port.write(self.encode(txBuffer))
        self.port.flush()
        stopTime= time.time()
        # print(f"Esse e o tempo final do experimento interface fisica: {stopTime-startTime}")
        return(nTx/2)

    def read(self, nBytes):
        """ Read nBytes from the UART com port

        Nem toda a leitura retorna múltiplo de 2
        devemos verificar isso para evitar que a funcao
        self.decode seja chamada com números ímpares.
        """
        rxBuffer = self.port.read(nBytes)
        rxBufferConcat = self.rxRemain + rxBuffer
        nValid = (len(rxBufferConcat)//2)*2
        rxBufferValid = rxBufferConcat[0:nValid]
        self.rxRemain = rxBufferConcat[nValid:]
        try :
            """ As vezes acontece erros na decodificacao
            fora do ambiente linux, isso tenta corrigir
            em parte esses erros. Melhorar futuramente."""
            rxBufferDecoded = self.decode(rxBufferValid)
            nRx = len(rxBuffer)
            return(rxBufferDecoded, nRx)
        except :
            print("[ERRO] interfaceFisica, read, decode. buffer : {}".format(rxBufferValid))
            return(b"", 0)

