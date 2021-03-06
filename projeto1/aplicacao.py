
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
serialName = "/dev/tty.usbmodem14101" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)

fileName = "jovicone.jpg"


print("porta COM aberta com sucesso")



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicaçao aberta")


    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso
    print ("gerando dados para transmissao :")
  
   
    with open(fileName,"rb") as img:
        f = img.read()
        b = bytearray(f)

    # print(f"joviro{b}")
    # ListTxBuffer =list()

    # for x in range(0,20):
    #     ListTxBuffer.append(x)

    txBuffer = b
    txLen    = len(txBuffer)
    print(txLen)
    # print(f"TxBuffer {txBuffer}")

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    com.sendData(txBuffer)

        
    # # Atualiza dados da transmissão
    # txSize = com.tx.getStatus()
   

    # # Faz a recepção dos dados
    # print ("Recebendo dados .... ")
    # bytesSeremLidos=com.rx.getBufferLen()
  
        
    # rxBuffer, nRx = com.getData(0)

    # # log
    # print ("Lido              {} bytes ".format(nRx))
    # # rxBuffer= list(rxBuffer)
    # # print ("rxbuffer",rxBuffer)

    # with open("./ImageRecebida.jpg","wb") as f:
    #     f.write((rxBuffer))

    

    # # Encerra comunicação
    # print("-------------------------")
    # print("Comunicaçao encerrada")
    # print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
