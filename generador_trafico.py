#!/usr/bin/env python3
from asterisk.ami import AMIClient, SimpleAction
import time
import random
import datetime
import json

AMI_HOST = '127.0.0.1'
AMI_PORT = 5038
AMI_USER = 'cybercall'
AMI_PASS = 'cyberpass'

EXTENSIONES_LEGITIMAS = ['6001', '6002', '6003']
EXTENSIONES_INEXISTENTES = ['9999', '8888', '7777', '6666', '5555']
DESTINOS_VALIDOS = ['5000', '8000']

stats = {
    'total': 0,
    'exitosas': 0,
    'fallidas': 0,
    'legitimas': 0,
    'maliciosas': 0
}

def hacer_llamada(origen, destino, espera=10000):
    try:
        client = AMIClient(address=AMI_HOST, port=AMI_PORT)
        client.login(username=AMI_USER, secret=AMI_PASS)
        action = SimpleAction('Originate', Channel=f'PJSIP/{origen}',
                              Context='default', Exten=destino, Priority=1,
                              CallerID=origen, Timeout=espera)
        client.send_action(action)
        client.logoff()
        if destino in DESTINOS_VALIDOS:
            stats['exitosas'] += 1
            return True
        else:
            stats['fallidas'] += 1
            return False
    except Exception as e:
        stats['fallidas'] += 1
        return False

def llamada_legitima():
    origen = random.choice(EXTENSIONES_LEGITIMAS)
    destino = random.choice(DESTINOS_VALIDOS)
    print(f"[LEGITIMO] {origen} -> {destino}")
    stats['legitimas'] += 1
    return hacer_llamada(origen, destino)

def ataque_fuerza_bruta():
    origen = '6001'
    destino = random.choice(EXTENSIONES_INEXISTENTES)
    print(f"[ATAQUE T1110] Fuerza bruta: {origen} -> {destino}")
    stats['maliciosas'] += 1
    return hacer_llamada(origen, destino)

def ataque_denegacion_servicio():
    origen = '6001'
    destino = '5000'
    print(f"[ATAQUE T1499] DoS: {origen} -> {destino}")
    stats['maliciosas'] += 1
    return hacer_llamada(origen, destino, espera=1000)

def ataque_toll_fraud():
    origen = random.choice(EXTENSIONES_LEGITIMAS)
    destino = '900123456'
    print(f"[ATAQUE T1078] Toll Fraud: {origen} -> {destino}")
    stats['maliciosas'] += 1
    return hacer_llamada(origen, destino)

def simulacion_mixta(duracion_segundos=30):
    inicio = time.time()
    comportamientos = [
        (llamada_legitima, 40),
        (ataque_fuerza_bruta, 30),
        (ataque_denegacion_servicio, 20),
        (ataque_toll_fraud, 10)
    ]
    
    print(f"\n🚀 Iniciando simulación por {duracion_segundos} segundos...")
    print("=" * 50)
    
    while time.time() - inicio < duracion_segundos:
        rand = random.randint(1, 100)
        acumulado = 0
        for func, prob in comportamientos:
            acumulado += prob
            if rand <= acumulado:
                func()
                stats['total'] += 1
                break
        time.sleep(random.uniform(0.5, 1.5))
    
    print("\n" + "=" * 50)
    print("📊 ESTADÍSTICAS FINALES")
    print(f"   Total eventos: {stats['total']}")
    print(f"   ✅ Exitosas: {stats['exitosas']}")
    print(f"   ❌ Fallidas: {stats['fallidas']}")
    print(f"   📞 Legítimas: {stats['legitimas']}")
    print(f"   💀 Maliciosas: {stats['maliciosas']}")
    print("=" * 50)

if __name__ == "__main__":
    print("🎯 CYBERCALL - Generador de Tráfico para SIEM")
    simulacion_mixta(30)
    print("\n✨ Simulación completada")
