
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

print("comecou")

from enlace import *
import time
# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/tty.usbmodem14401"# Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)

fileName = "jovicone.jpg"


print("porta COM aberta com sucesso")




def receiveInfo():

    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicaçao aberta")
    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    bytesSeremLidos=com.rx.getBufferLen()
  
        
    rxBuffer, nRx = com.getData(10  )

    # log
    print ("Lido              {} bytes ".format(nRx))
    # rxBuffer= list(rxBuffer)
    # print ("rxbuffer",rxBuffer)

    print(f"Tamanho da imagem: {nRx} bytes")
    print(f"Tempo suposto de envio: {com.supposedTime(nRx)} ms")


    with open("./ImageRecebida.jpg","wb") as f:
        f.write((rxBuffer))

    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicaçao encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    receiveInfo()
