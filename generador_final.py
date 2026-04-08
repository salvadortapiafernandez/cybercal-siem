import socket
import time
import random
import threading

class AMIClient:
    def __init__(self):
        self.socket = None
        self.connected = False
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 5038))
        self.socket.send(b'Action: Login\r\nUsername: admin\r\nSecret: mi_password\r\n\r\n')
        response = self.socket.recv(4096).decode()
        if 'Authentication accepted' in response:
            self.connected = True
            print("✅ Conectado a Asterisk AMI")
            return True
        return False
    
    def originate(self, origen, destino, timeout=30000):
        if not self.connected:
            return False
        cmd = f'Action: Originate\r\nChannel: PJSIP/{origen}\r\nContext: default\r\nExten: {destino}\r\nPriority: 1\r\nCallerID: {origen}\r\nTimeout: {timeout}\r\n\r\n'
        self.socket.send(cmd.encode())
        response = self.socket.recv(4096).decode()
        return 'Success' in response
    
    def close(self):
        if self.socket:
            self.socket.send(b'Action: Logoff\r\n\r\n')
            self.socket.close()
            self.connected = False

# Inicializar cliente
cliente = AMIClient()
if not cliente.connect():
    print("❌ No se pudo conectar")
    exit(1)

print("\n🎯 CYBERCALL - Generador de Tráfico para SIEM")
print("   Simula: Tráfico legítimo + Ataques MITRE\n")

stats = {'total': 0, 'exitosas': 0, 'legitimas': 0, 'maliciosas': 0}

try:
    while True:
        # Elegir tipo de evento
        tipo = random.choices(
            ['legitimo', 'bruteforce', 'tollfraud', 'dos'],
            weights=[40, 30, 15, 15]
        )[0]
        
        if tipo == 'legitimo':
            origen = random.choice(['6001', '6002', '6003'])
            destino = random.choice(['5000', '8000'])
            print(f"[LEGITIMO] {origen} -> {destino}")
            exito = cliente.originate(origen, destino)
            stats['legitimas'] += 1
        
        elif tipo == 'bruteforce':
            origen = '6001'
            destino = random.choice(['5555', '6666', '7777', '8888', '9999'])
            print(f"[ATAQUE T1110] Fuerza bruta: {origen} -> {destino}")
            exito = cliente.originate(origen, destino, timeout=5000)
            stats['maliciosas'] += 1
        
        elif tipo == 'tollfraud':
            origen = random.choice(['6001', '6002'])
            destino = '900123456'
            print(f"[ATAQUE T1078] Toll Fraud: {origen} -> {destino}")
            exito = cliente.originate(origen, destino)
            stats['maliciosas'] += 1
        
        else:  # dos
            origen = '6001'
            destino = '5000'
            print(f"[ATAQUE T1499] DoS: {origen} -> {destino} (3 llamadas rápidas)")
            for _ in range(3):
                cliente.originate(origen, destino, timeout=5000)
                time.sleep(0.1)
            exito = True
            stats['maliciosas'] += 1
        
        stats['total'] += 1
        if exito:
            stats['exitosas'] += 1
        
        time.sleep(random.uniform(0.5, 1.5))

except KeyboardInterrupt:
    print("\n\n" + "="*50)
    print("📊 ESTADÍSTICAS FINALES")
    print(f"   Total eventos: {stats['total']}")
    print(f"   ✅ Exitosas: {stats['exitosas']}")
    print(f"   ❌ Fallidas: {stats['total'] - stats['exitosas']}")
    print(f"   📞 Legítimas: {stats['legitimas']}")
    print(f"   💀 Maliciosas: {stats['maliciosas']}")
    print("="*50)
    cliente.close()
    print("\n✨ Simulación completada")
