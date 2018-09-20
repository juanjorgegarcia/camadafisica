#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# JJ e Guigui
# 30/08/2018
#  Main
####################################################

from enlace import *
import time
import comunicator
from sys import argv

  

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/cu.usbmodem14101"  # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)

fileName = "./joji.jpg"




def main():
    
    c = comunicator.Comunicator(argv[2],argv[1])

    c.startCom()

    print("porta COM aberta com sucesso")

    c.waitForResponse()


    # Encerra comunicação
    print("-------------------------")
    print("Comunicaçao encerrada")
    print("-------------------------")

if __name__ == "__main__":
    main()