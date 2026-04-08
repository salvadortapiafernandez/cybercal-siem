#!/usr/bin/env python3
import time
import random
import sys
from asterisk.ami import AMIClient, SimpleAction

# Configuración AMI
AMI_HOST = 'localhost'
AMI_PORT = 5038
AMI_USER = 'admin'
AMI_PASS = 'mi_password'

# Conectar UNA SOLA VEZ
print("🔌 Conectando a Asterisk AMI...")
client = AMIClient(address=AMI_HOST, port=AMI_PORT)
client.login(username=AMI_USER, secret=AMI_PASS)
print("✅ Conectado\n")

def hacer_llamada(origen, destino, tiempo_espera=30000):
    try:
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
        return response.is_success()
    except Exception as e:
        print(f"  Error: {e}")
        return False

def llamada_legitima():
    origen = random.choice(['6001', '6002', '6003'])
    destino = random.choice(['5000', '8000', '5000'])
    exito = hacer_llamada(origen, destino)
    print(f"[LEGITIMO] {origen} -> {destino} {'✅' if exito else '❌'}")
    return exito

def ataque_fuerza_bruta():
    origen = '6001'
    destino = random.choice(['5555', '6666', '7777', '8888', '9999'])
    exito = hacer_llamada(origen, destino)
    print(f"[ATAQUE T1110] Fuerza bruta: {origen} -> {destino} {'✅' if exito else '❌'}")
    return exito

def ataque_toll_fraud():
    origen = random.choice(['6001', '6002', '6003'])
    destino = '900123456'
    exito = hacer_llamada(origen, destino)
    print(f"[ATAQUE T1078] Toll Fraud: {origen} -> {destino} {'✅' if exito else '❌'}")
    return exito

def ataque_dos():
    origen = '6001'
    destino = '5000'
    # Múltiples llamadas rápidas para simular DoS
    for i in range(3):
        hacer_llamada(origen, destino, 5000)
    print(f"[ATAQUE T1499] DoS: {origen} -> {destino} (3 llamadas rápidas)")
    return True

# Comportamientos y sus probabilidades
comportamientos = [
    (llamada_legitima, 40),      # 40% legítimo
    (ataque_fuerza_bruta, 30),   # 30% fuerza bruta
    (ataque_toll_fraud, 15),     # 15% toll fraud
    (ataque_dos, 15)             # 15% DoS
]

stats = {'total': 0, 'exitosas': 0, 'fallidas': 0, 'legitimas': 0, 'maliciosas': 0}

print("🎯 CYBERCALL - Generador de Tráfico para SIEM")
print("   Simula: Tráfico legítimo + Ataques MITRE\n")
print("🚀 Iniciando simulación (Ctrl+C para detener)")
print("=" * 50)

try:
    contador = 0
    while True:
        rand = random.randint(1, 100)
        acumulado = 0
        
        for func, prob in comportamientos:
            acumulado += prob
            if rand <= acumulado:
                exito = func()
                stats['total'] += 1
                if exito:
                    stats['exitosas'] += 1
                else:
                    stats['fallidas'] += 1
                
                if func.__name__ == 'llamada_legitima':
                    stats['legitimas'] += 1
                else:
                    stats['maliciosas'] += 1
                break
        
        contador += 1
        time.sleep(random.uniform(0.5, 1.5))
        
        # Mostrar estadísticas cada 10 iteraciones
        if contador % 10 == 0:
            print(f"\n📊 [{contador}] OK:{stats['exitosas']} ERR:{stats['fallidas']} Leg:{stats['legitimas']}/Mal:{stats['maliciosas']}\n")

except KeyboardInterrupt:
    print("\n" + "=" * 50)
    print("📊 ESTADÍSTICAS FINALES")
    print(f"   Total eventos: {stats['total']}")
    print(f"   ✅ Exitosas: {stats['exitosas']}")
    print(f"   ❌ Fallidas: {stats['fallidas']}")
    print(f"   📞 Legítimas: {stats['legitimas']}")
    print(f"   💀 Maliciosas: {stats['maliciosas']}")
    print("=" * 50)
    print("\n🔌 Cerrando conexión...")
    client.logoff()
    print("✨ Simulación completada")
