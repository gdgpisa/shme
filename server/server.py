#coding=utf-8
import json
from SimpleWebSocketServer import SimpleSSLWebSocketServer, WebSocket
import ssl
import RPi.GPIO as GPIO

clients = [] #array dei client che hanno effettuato login
pinstate ={"triforce":1} #il server parte supponendo tutto spento

##################################
#SEZIONE SOLO A SCOPO DIMOSTRATIVO
idlogin="GDG"
pwlogin="Pisa"
##################################

LoginOkMessage='{"code":200, "text":"Login OK"}'
LoginFailedMessage='{"code":400, "text":"Login Fallito"}'
LoginNecessaryMessage='{"code":400, "text":"Necessario Login"}'
AffermativeMessage='{"code":200, "text":"OK"}'
NegativeMessage='{"code":400, "text":"Operazione non riuscita"}'

#Inizio WebSocket
class SimpleServer(WebSocket):

    def handleMessage(self):
        try:
            data=json.loads(self.data)

            #richiesta di login
            if (int(data["code"])==0):

                if(str(data["id"])==idlogin and str(data["pw"])==pwlogin ):
                    
                    clients.append(self)
                    self.sendMessage(str(LoginOkMessage))
                    #aggiorno client su stato bottoni
                    updateClient(self)

                else:
                    self.sendMessage(str(LoginFailedMessage))

            #messaggio dal client
            elif (int(data["code"])==100):

                index=-1
                try:
                    index=clients.index(self)
                except:
                     self.sendMessage(LoginNecessaryMessage)

                #se client loggato
                if(index>(-1)):
                    try:
                        portWrite(portMap(str(data["op"])),str(data["val"]))
                        pinstate[str(data["op"])]=int(data["val"])
                        self.sendMessage(AffermativeMessage)
                        for client in clients:
                            client.sendMessage(self.data)

                    except Exception as e:
                        print(e)
                        self.sendMessage(NegativeMessage)

        except Exception as e: 
            print "Messaggio malformato, scartato"
            print self.data
            print(e)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')
        try:
            index=clients.index(self)
            clients.remove(index)
            print "Client loggato disconnesso"
        except:
            print "Client non loggato disconnesso"

def updateClient(self):
    message={"code":101,"op":["a"],"val":[0]}
    count=0
    for state in pinstate:
        message["op"][count]=state
        message["val"][count]=pinstate[state]
        count=count+1
    
    print json.dumps(message)
    self.sendMessage(json.dumps(message))
        
#Fine WebSocket
	
#Inizializzazione porte GPIO sia in input che output
GPIO.setmode(GPIO.BCM)
for(key, value) in enumerate([26]):
    GPIO.setup(value, GPIO.OUT)

#Le porte GPIO vengono disattivate.
#N.B. HIGH=1=Porta GPIO spenta, LOW=0=Porta GPIO accesa
GPIO.output([26], GPIO.HIGH)

def portMap(val):
    if val=="triforce":
        return 26

#Scrittura valori sulle porte GPIO in base al valore
def portWrite(porta,stato):
    porta=int(porta)
    if stato=='1':
        GPIO.output(porta,GPIO.HIGH)
    if stato=='0':
        GPIO.output(porta,GPIO.LOW)
    if stato=='-1':
        GPIO.output(porta, not GPIO.input(porta))
    print("Stato cambiato:"+str(GPIO.input(porta)))
    return(GPIO.input(porta))

try: 
    if __name__ == '__main__':
        server = SimpleSSLWebSocketServer('0.0.0.0', 5000, SimpleServer,'/etc/letsencrypt/live/my.awesome.domain/cert.pem','/etc/letsencrypt/live/my.awesome.domain/privkey.pem',ssl.PROTOCOL_TLSv1)
        server.serveforever()

except KeyboardInterrupt:
    GPIO.cleanup()
    print "cleaning up gpio before closing"
