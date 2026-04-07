#!/usr/bin/env python3
from asterisk.ami import AMIClient, SimpleAction
import time

AMI_HOST = '127.0.0.1'
AMI_PORT = 5038
AMI_USER = 'cybercall'
AMI_PASS = 'cyberpass'

def hacer_llamada(origen, destino, tiempo_espera=30000):
    try:
        client = AMIClient(address=AMI_HOST, port=AMI_PORT)
        client.login(username=AMI_USER, secret=AMI_PASS)
        print(f"Llamada: {origen} -> {destino}")
        
        action = SimpleAction(
            'Originate',
            Channel=f'PJSIP/{origen}',
            Context='default',
            Exten=destino,
            Priority=1,
            CallerID=origen,
            Timeout=tiempo_espera
        )
        
        response = client.send_action(action)
        print("Llamada completada")
        client.logoff()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Generador de Llamadas - CyberCall")
    hacer_llamada('6001', '5000')
    print("Script finalizado")
