import socket

def test_ami():
    try:
        # Conectar
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 5038))
        
        # Login
        login_cmd = "Action: Login\r\nUsername: admin\r\nSecret: mi_password\r\n\r\n"
        s.send(login_cmd.encode())
        
        # Recibir respuesta
        response = s.recv(4096).decode()
        print("Respuesta del servidor:")
        print(response)
        
        if "Authentication accepted" in response:
            print("\n✅ Conexión exitosa con Asterisk!")
        else:
            print("\n❌ Falló la autenticación")
        
        # Logoff
        s.send(b"Action: Logoff\r\n\r\n")
        s.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ami()
