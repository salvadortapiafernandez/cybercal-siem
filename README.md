

# 📞 CyberCall - De Ejecutivo Callcenter a Ciberdefensor

> *"De tomar llamadas en el Banco Estado a defenderlas con código"*

## 🎯 La Historia Real

Corría el año 2024 cuando trabajaba como ejecutivo en el callcenter del **Banco Estado**. 
Día tras día, atendía clientes, resolvía dudas y veía cómo operaba la central telefónica. 
Pero también fui testigo de algo más oscuro: clientes que reportaban cargos no reconocidos, 
números extraños que aparecían en sus cuentas, y llamadas que nunca hicieron.

Ahí entendí una verdad incómoda: **los callcenters son un blanco perfecto para ciberataques**.

- Ataques de **fuerza bruta** a extensiones (T1110)
- **Toll fraud** con llamadas a números premium (T1078)
- **Denegación de servicio** colapsando líneas (T1499)

Esa experiencia me motivó a estudiar ciberseguridad. Hoy, como Técnico en Ciberseguridad 
y estudiante de Ingeniería, construí este laboratorio para simular exactamente esos ataques 
y mostrar cómo un **SIEM** (como Wazuh) puede detectarlos en tiempo real.

Este proyecto es mi forma de decir: **sé cómo atacan, y sé cómo defender**.

---

## 🏗️ Arquitectura del Laboratorio

┌─────────────────────────────────────────────────────────────┐
│ NOTEBOOK PRINCIPAL (SIEM) │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│ │ Asterisk │ │ Wazuh │ │ Python Scripts │ │
│ │ (Callcenter)│ │ (SIEM) │ │ generador_simple.py│ │
│ └─────────────┘ └─────────────┘ └─────────────────────┘ │
│ │ │ │ │
│ └───────────────┼────────────────────┘ │
│ │ │
└─────────────────────────┼───────────────────────────────────┘
│
┌────┴────┐
│ Router │
│ de Casa│
└────┬────┘
│
┌─────────────────────────┼───────────────────────────────────┐
│ NOTEBOOK MAMÁ (KALI) │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ nmap │ hydra │ hping3 │ sipcrack ││
│ └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
text


---

## 🚀 Ataques Simulados (MITRE ATT&CK)

| Técnica | Nombre | Simulación |
|---------|--------|------------|
| **T1110** | Fuerza Bruta | Múltiples intentos a extensiones 5555,6666,7777,8888,9999 |
| **T1078** | Toll Fraud | Llamadas a números de tarificación adicional (900123456) |
| **T1499** | DoS | 3 llamadas rápidas al mismo destino para saturar líneas |

---

## 📦 Requisitos

- **Docker** y **Docker Compose**
- **Python 3.13+**
- **8 GB RAM** (recomendado)
- **Linux/Kali** (para ataques)

---

## 🛠️ Instalación Paso a Paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/salvadortapiafernandez/cybercal-siem.git
cd cybercal-siem

2. Crear entorno virtual Python
bash

python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

3. Instalar dependencias
bash

pip install pyst2

4. Levantar Asterisk (Callcenter)
bash

docker run -d --name asterisk -p 5038:5038 -p 5060:5060/udp andrius/asterisk:latest
sleep 10
docker exec asterisk bash -c 'cat > /etc/asterisk/manager.conf << EOF
[general]
enabled = yes
port = 5038
bindaddr = 0.0.0.0

[admin]
secret = mi_password
permit = 0.0.0.0/0.0.0.0
read = all
write = all
EOF'
docker exec asterisk asterisk -rx "module reload manager"

5. Levantar Wazuh (SIEM)
bash

cd wazuh-stack
docker-compose up -d

6. Ejecutar el generador de tráfico
bash

cd ~/cybercal-siem
source venv/bin/activate
python generador_simple.py

🌐 Acceder al Dashboard de Wazuh

    URL: https://localhost

    Usuario: admin

    Contraseña: SecretPassword

💀 Desde Kali (Máquina Atacante)
bash

# Escanear puertos SIP y AMI
nmap -p 5038,5060 <IP_DEL_SIEM>

# Ataque de fuerza bruta a extensiones
hydra -l 6001 -P /usr/share/wordlists/rockyou.txt sip://<IP_DEL_SIEM>

# Denegación de servicio (DoS)
hping3 --udp --flood -p 5060 <IP_DEL_SIEM>

📊 Estadísticas de Ejemplo
text

==================================================
📊 ESTADÍSTICAS FINALES
   Total eventos: 32
   ✅ Exitosas: 19
   ❌ Fallidas: 13
   📞 Legítimas: 8
   💀 Maliciosas: 24
==================================================

🧠 Lecciones Aprendidas

    Los logs no mienten - Wazuh detectó cada ataque

    Automatización es poder - Python + AMI = simulación realista

    El contexto importa - Saber cómo opera un callcenter ayuda a defenderlo

    Purple Team funciona - Atacar y defender te hace mejor profesional

📁 Estructura del Proyecto
text

cybercal-siem/
├── generador_simple.py      # Script principal (funcionando)
├── test_ami.py              # Prueba de conexión AMI
├── wazuh-stack/             # Configuración completa de Wazuh
│   └── docker-compose.yml
├── venv/                    # Entorno virtual Python
└── README.md                # Este archivo

🙋‍♂️ Sobre el Autor

Salvador Tapia Fernández

    Técnico en Ciberseguridad (egresado)

    Estudiante de Ingeniería en Ciberseguridad

    Ex ejecutivo callcenter Banco Estado

"De tomar llamadas a protegerlas. La mejor defensa es entender cómo atacan."
📄 Licencia

MIT - Libre para aprender, compartir y mejorar.
⭐ ¿Te sirvió?

Si este proyecto te ayudó a entender cómo funcionan los ataques a callcenters,
dame una estrella ⭐ en GitHub. ¡Construyamos juntos un ciberespacio más seguro!

Proyecto creado con ❤️ desde Chile
text


## 📌 Instrucciones para pegarlo:

1. Ve a tu repositorio en GitHub: `https://github.com/salvadortapiafernandez/cybercal-siem`
2. Haz clic en el archivo `README.md`
3. Haz clic en el lápiz (editar)
4. Borra todo el contenido
5. **Pega todo el texto de arriba**
6. Haz clic en **"Commit changes"** (verde abajo)

## 🎯 ¡Y LISTO!

Tu README quedará profesional, con tu historia, comandos y todo. **Pégalo tal cual, no modifiques nada.** 🔥

pero necesito todo en uno sin los bash pues para copiarlo pues

¡Claro, mi bro! Aquí está el README PURITO, sin los ```bash, solo el texto plano para que copies y pegues directo:
📞 CyberCall - De Ejecutivo Callcenter a Ciberdefensor

    "De tomar llamadas en el Banco Estado a defenderlas con código"

🎯 La Historia Real

Corría el año 2024 cuando trabajaba como ejecutivo en el callcenter del Banco Estado.
Día tras día, atendía clientes, resolvía dudas y veía cómo operaba la central telefónica.
Pero también fui testigo de algo más oscuro: clientes que reportaban cargos no reconocidos,
números extraños que aparecían en sus cuentas, y llamadas que nunca hicieron.

Ahí entendí una verdad incómoda: los callcenters son un blanco perfecto para ciberataques.

    Ataques de fuerza bruta a extensiones (T1110)

    Toll fraud con llamadas a números premium (T1078)

    Denegación de servicio colapsando líneas (T1499)

Esa experiencia me motivó a estudiar ciberseguridad. Hoy, como Técnico en Ciberseguridad
y estudiante de Ingeniería, construí este laboratorio para simular exactamente esos ataques
y mostrar cómo un SIEM (como Wazuh) puede detectarlos en tiempo real.

Este proyecto es mi forma de decir: sé cómo atacan, y sé cómo defender.
🏗️ Arquitectura del Laboratorio
text

┌─────────────────────────────────────────────────────────────┐
│                    NOTEBOOK PRINCIPAL (SIEM)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Asterisk   │  │    Wazuh    │  │   Python Scripts    │ │
│  │  (Callcenter)│  │   (SIEM)    │  │  generador_simple.py│ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│         │               │                    │              │
│         └───────────────┼────────────────────┘              │
│                         │                                   │
└─────────────────────────┼───────────────────────────────────┘
                          │
                     ┌────┴────┐
                     │  Router │
                     │  de Casa│
                     └────┬────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                    NOTEBOOK MAMÁ (KALI)                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  nmap │ hydra │ hping3 │ sipcrack                      ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘

🚀 Ataques Simulados (MITRE ATT&CK)
Técnica	Nombre	Simulación
T1110	Fuerza Bruta	Múltiples intentos a extensiones 5555,6666,7777,8888,9999
T1078	Toll Fraud	Llamadas a números de tarificación adicional (900123456)
T1499	DoS	3 llamadas rápidas al mismo destino para saturar líneas
📦 Requisitos

    Docker y Docker Compose

    Python 3.13+

    8 GB RAM (recomendado)

    Linux/Kali (para ataques)

🛠️ Instalación Paso a Paso
1. Clonar el repositorio

git clone https://github.com/salvadortapiafernandez/cybercal-siem.git
cd cybercal-siem
2. Crear entorno virtual Python

python3 -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
3. Instalar dependencias

pip install pyst2
4. Levantar Asterisk (Callcenter)

docker run -d --name asterisk -p 5038:5038 -p 5060:5060/udp andrius/asterisk:latest
sleep 10
docker exec asterisk bash -c 'cat > /etc/asterisk/manager.conf << EOF
[general]
enabled = yes
port = 5038
bindaddr = 0.0.0.0

[admin]
secret = mi_password
permit = 0.0.0.0/0.0.0.0
read = all
write = all
EOF'
docker exec asterisk asterisk -rx "module reload manager"
5. Levantar Wazuh (SIEM)

cd wazuh-stack
docker-compose up -d
6. Ejecutar el generador de tráfico

cd ~/cybercal-siem
source venv/bin/activate
python generador_simple.py
🌐 Acceder al Dashboard de Wazuh

    URL: https://localhost

    Usuario: admin

    Contraseña: SecretPassword

💀 Desde Kali (Máquina Atacante)
Escanear puertos SIP y AMI

nmap -p 5038,5060 <IP_DEL_SIEM>
Ataque de fuerza bruta a extensiones

hydra -l 6001 -P /usr/share/wordlists/rockyou.txt sip://<IP_DEL_SIEM>
Denegación de servicio (DoS)

hping3 --udp --flood -p 5060 <IP_DEL_SIEM>
📊 Estadísticas de Ejemplo

==================================================
📊 ESTADÍSTICAS FINALES
Total eventos: 32
✅ Exitosas: 19
❌ Fallidas: 13
📞 Legítimas: 8
💀 Maliciosas: 24
==================================================
🧠 Lecciones Aprendidas

    Los logs no mienten - Wazuh detectó cada ataque

    Automatización es poder - Python + AMI = simulación realista

    El contexto importa - Saber cómo opera un callcenter ayuda a defenderlo

    Purple Team funciona - Atacar y defender te hace mejor profesional

📁 Estructura del Proyecto

cybercal-siem/
├── generador_simple.py # Script principal (funcionando)
├── test_ami.py # Prueba de conexión AMI
├── wazuh-stack/ # Configuración completa de Wazuh
│ └── docker-compose.yml
├── venv/ # Entorno virtual Python
└── README.md # Este archivo
🙋‍♂️ Sobre el Autor

Salvador Tapia Fernández

    Técnico en Ciberseguridad (egresado)

    Estudiante de Ingeniería en Ciberseguridad

    Ex ejecutivo callcenter Banco Estado

"De tomar llamadas a protegerlas. La mejor defensa es entender cómo atacan."
📄 Licencia

MIT - Libre para aprender, compartir y mejorar.
⭐ ¿Te sirvió?

Si este proyecto te ayudó a entender cómo funcionan los ataques a callcenters,
dame una estrella ⭐ en GitHub. ¡Construyamos juntos un ciberespacio más seguro!

Proyecto creado con ❤️ desde Chile
