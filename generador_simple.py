import socket
import time
import random

def send_ami_command(cmd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 5038))
        # Login
        s.send(b'Action: Login\r\nUsername: admin\r\nSecret: mi_password\r\n\r\n')
        response = s.recv(4096).decode()
        
        if 'Authentication accepted' not in response:
            return False
        
        # Enviar comando
        s.send(cmd.encode())
        result = s.recv(4096).decode()
        s.close()
        return 'Success' in result
    except Exception as e:
        print(f"Error: {e}")
        return False

def hacer_llamada(origen, destino, timeout=30000):
    cmd = f'Action: Originate\r\nChannel: PJSIP/{origen}\r\nContext: default\r\nExten: {destino}\r\nPriority: 1\r\nCallerID: {origen}\r\nTimeout: {timeout}\r\n\r\n'
    return send_ami_command(cmd)

print("🎯 CYBERCALL - Generador de Tráfico para SIEM")
print("   Simula: Tráfico legítimo + Ataques MITRE\n")
print("🚀 Iniciando simulación (Ctrl+C para detener)\n")

stats = {'total': 0, 'exitosas': 0, 'legitimas': 0, 'maliciosas': 0}

try:
    while True:
        tipo = random.choices(
            ['legitimo', 'bruteforce', 'tollfraud', 'dos'],
            weights=[40, 30, 15, 15]
        )[0]
        
        if tipo == 'legitimo':
            origen = random.choice(['6001', '6002', '6003'])
            destino = random.choice(['5000', '8000'])
            print(f"[LEGITIMO] {origen} -> {destino}")
            exito = hacer_llamada(origen, destino)
            stats['legitimas'] += 1
        
        elif tipo == 'bruteforce':
            origen = '6001'
            destino = random.choice(['5555', '6666', '7777', '8888', '9999'])
            print(f"[ATAQUE T1110] Fuerza bruta: {origen} -> {destino}")
            exito = hacer_llamada(origen, destino, timeout=5000)
            stats['maliciosas'] += 1
        
        elif tipo == 'tollfraud':
            origen = random.choice(['6001', '6002'])
            destino = '900123456'
            print(f"[ATAQUE T1078] Toll Fraud: {origen} -> {destino}")
            exito = hacer_llamada(origen, destino)
            stats['maliciosas'] += 1
        
        else:  # dos
            origen = '6001'
            destino = '5000'
            print(f"[ATAQUE T1499] DoS: {origen} -> {destino}")
            for _ in range(3):
                hacer_llamada(origen, destino, timeout=5000)
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
    print("\n✨ Simulación completada")
