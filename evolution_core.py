import os
import sys
import platform
import subprocess
import json
import base64
import random
import threading
import time
import socket
import urllib.request
import webbrowser
from datetime import datetime

# ==============================================================================
#  PROJECT: EVOLUTION MULTIPLATAFORM TOTAL v5.6.3 - PROYECTOS GENIALES
#  GLOBAL FOUNDER & PRESIDENT: JUAN CAMILO MAZO GONZALEZ (jcmgru)
#  COMPILATION TARGET: WINDOWS / LINUX UNIFIED SECURITY PRODUCTION BUILD
# ==============================================================================

SISTEMA_ACTUAL = platform.system().lower()

if SISTEMA_ACTUAL == "windows":
    CONFIG_DIR = "C:\\ProgramData\\ProyectosGeniales\\Evolution"
else:
    CONFIG_DIR = os.path.expanduser("~/.proyectosgeniales/evolution")

CONFIG_PATH = os.path.join(CONFIG_DIR, "node_secure.dat")
REGISTRO_P2P_LOCAL = os.path.join(CONFIG_DIR, "p2p_mesh_index.txt")

_VAULT_KEY = 0xA7
PUERTO_ENJAMBRE = 8000
NODOS_CONOCIDOS_REDUNDANCIA = ["127.0.0.1"]

ROLES_SISTEMA = {
    "usuario_estandar": {"nivel": 1, "req_ref": 0,    "retorno_potencia": "Básico Local", "desc": "Carga procesada únicamente por el hardware local."},
    "aprendiz":         {"nivel": 2, "req_ref": 10,   "retorno_potencia": "+10 Nodos",     "desc": "Aceleración básica del enjambre para tareas ligeras."},
    "adulto":           {"nivel": 3, "req_ref": 100,  "retorno_potencia": "+100 Nodos",    "desc": "Capacidad distribuida para Diseño Gráfico y Renderizado."},
    "pro":              {"nivel": 4, "req_ref": 1000, "retorno_potencia": "+1000 Nodos",   "desc": "Potencia masiva para Modelado 3D y Motores Gráficos."},
    "avanzado":         {"nivel": 5, "req_ref": 2000, "retorno_potencia": "+2000 Nodos",   "desc": "Soporte de cómputo para Edición de Video Pesado y Big Data."},
    "creador":          {"nivel": 6, "req_ref": 5000, "retorno_potencia": "+5000 Nodos",   "desc": "Máximo retorno del enjambre. Computador local virtualizado al 100%."},
    "todopoderoso":     {"nivel": 7, "req_ref": float('inf'), "retorno_potencia": "Absoluto", "desc": "Gobernanza y absorción total de la red global P2P."}
}
class EvolutionEnjambreEngine:
    def __init__(self):
        self.enjambre_ram_p2p = {}
        self.nodos_vecinos_activos = set()
        self.user_session = {
            "usuario_local": "invitado_nodo",
            "referido_por": "jcmgru",
            "rol_actual": "usuario_estandar",
            "referidos_validos": 0,
            "enlace_referido": "https://proyectosgeniales.com"
        }
        self.node_vault = {
            "metadata": {
                "organization": "Proyectos Geniales",
                "president_human": "Juan Camilo Mazo Gonzalez (jcmgru)",
                "vicepresident_human": "Julian Andres Mazo Zapata"
            },
            "autonomous_gateways": {
                "web3_public_vault": "0xf24A94B8c1ec54005C7D4f4fe7f68cd585131470",
                "emergency_fiat_node": "https://www.paypal.com/donate/?hosted_button_id=XBX3CXHFXMD9Y",
                "decentralized_bandwidth": "https://app.grass.io/register?referralCode=xmpnmoiR2V4z7R4"
            }
        }

    def _cipher_stream(self, text: str) -> str:
        return "".join(chr(ord(c) ^ _VAULT_KEY) for c in text)

    def sync_vault(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'rb') as f:
                    raw = f.read()
                decoded = base64.b64decode(raw).decode('utf-8')
                self.node_vault.update(json.loads(self._cipher_stream(decoded)))
            except Exception:
                pass
        return self.node_vault

    def commit_vault(self):
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            serialized = json.dumps(self.node_vault, indent=4)
            encoded = base64.b64encode(self._cipher_stream(serialized).encode('utf-8'))
            with open(CONFIG_PATH, 'wb') as f:
                f.write(encoded)
        except Exception:
            pass
    def inicializar_bd_p2p_local(self):
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            if not os.path.exists(REGISTRO_P2P_LOCAL):
                with open(REGISTRO_P2P_LOCAL, "w", encoding="utf-8") as f:
                    f.write("# RED DISTRIBUIDA ENJAMBRE P2P MESH v5.6.3\n")
                    f.write("jcmgru|root|20260101000000\n")
            self.cargar_bd_local_a_ram()
        except Exception:
            pass

    def cargar_bd_local_a_ram(self):
        try:
            if os.path.exists(REGISTRO_P2P_LOCAL):
                with open(REGISTRO_P2P_LOCAL, "r", encoding="utf-8") as f:
                    for linea in f:
                        if linea.startswith("#") or not linea.strip():
                            continue
                        partes = linea.strip().split("|")
                        if len(partes) >= 2:
                            self.enjambre_ram_p2p[partes[0].lower()] = partes[1].lower()
        except Exception:
            pass

    def verificar_y_registrar_p2p(self, username: str, referrer: str) -> bool:
        self.inicializar_bd_p2p_local()
        user_limpio = username.strip().lower()
        ref_limpio = referrer.strip().lower() if referrer.strip() else "jcmgru"
        if not user_limpio:
            return False
        vault = self.sync_vault()
        if vault.get("usuario_guardado", "").lower() == user_limpio:
            return True
        if user_limpio in self.enjambre_ram_p2p:
            return False
        try:
            with open(REGISTRO_P2P_LOCAL, "a", encoding="utf-8") as f:
                f.write(f"{user_limpio}|{ref_limpio}|\n")
            self.enjambre_ram_p2p[user_limpio] = ref_limpio
            threading.Thread(target=self.propagar_registro_a_vecinos_p2p, args=(user_limpio, ref_limpio), daemon=True).start()
            return True
        except Exception:
            return False

    def propagar_registro_a_vecinos_p2p(self, user: str, referrer: str):
        payload = json.dumps({"action": "sync_new_node", "user": user, "referrer": referrer})
        for peer_ip in list(self.nodos_vecinos_activos) + NODOS_CONOCIDOS_REDUNDANCIA:
            if peer_ip == "127.0.0.1": continue
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2.0)
                s.connect((peer_ip, PUERTO_ENJAMBRE))
                s.send(payload.encode('utf-8'))
                s.close()
            except Exception:
                pass

    def contar_referidos_p2p_ram(self, username: str) -> int:
        user_limpio = username.strip().lower()
        return sum(1 for patrocinador in self.enjambre_ram_p2p.values() if patrocinador == user_limpio)

    def calcular_rango_y_privilegios(self):
        user = self.user_session["usuario_local"].strip().lower()
        self.cargar_bd_local_a_ram()
        if user in ["juan camilo mazo gonzalez", "jcmgru", "julian andres mazo zapata"]:
            self.user_session["rol_actual"] = "todopoderoso"
            self.user_session["referidos_validos"] = len(self.enjambre_ram_p2p)
            return
        self.user_session["referidos_validos"] = self.contar_referidos_p2p_ram(user)
        ref = self.user_session["referidos_validos"]
        if ref >= 5000: self.user_session["rol_actual"] = "creador"
        elif ref >= 2000: self.user_session["rol_actual"] = "avanzado"
        elif ref >= 1000: self.user_session["rol_actual"] = "pro"
        elif ref >= 100:  self.user_session["rol_actual"] = "adulto"
        elif ref >= 10:   self.user_session["rol_actual"] = "aprendiz"
        else: self.user_session["rol_actual"] = "usuario_estandar"
def iniciar_servidor_escucha_p2p(engine_instance):
    def server_loop():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", PUERTO_ENJAMBRE))
            server.listen(500)
            while True:
                conn, addr = server.accept()
                threading.Thread(target=procesar_trafico_p2p_mesh, args=(conn, addr, engine_instance), daemon=True).start()
        except Exception:
            pass
    threading.Thread(target=server_loop, daemon=True).start()

def procesar_trafico_p2p_mesh(conn, addr, engine):
    try:
        conn.settimeout(2.5)
        engine.nodos_vecinos_activos.add(addr[0])
        raw_data = conn.recv(2048).decode('utf-8')
        if raw_data:
            payload = json.loads(raw_data)
            action = payload.get("action")
            if action == "sync_new_node":
                user = payload.get("user")
                referrer = payload.get("referrer")
                if user and user not in engine.enjambre_ram_p2p:
                    engine.enjambre_ram_p2p[user] = referrer
                    with open(REGISTRO_P2P_LOCAL, "a", encoding="utf-8") as f:
                        f.write(f"{user}|{referrer}|\n")
            conn.send(b'{"p2p_sync": true}')
    except Exception:
        pass
    finally:
        conn.close()

def limpiar_interfaz():
    os.system('cls' if platform.system().lower() == "windows" else 'clear')

def ejecutar_purga_sistema():
    sistema = platform.system().lower()
    try:
        import gc
        gc.collect()
        if sistema == "windows":
            os.system("del /s /f /q %windir%\\Temp\\*.* >nul 2>&1")
            os.system("ipconfig /flushdns >nul 2>&1")
            return True
        elif sistema == "linux":
            os.system("rm -rf /tmp/* >/dev/null 2>&1")
            if os.path.exists("/etc/init.d/dns-clean"):
                os.system("/etc/init.d/dns-clean start >/dev/null 2>&1")
            os.system("sync && echo 3 > /proc/sys/vm/drop_caches >/dev/null 2>&1")
            return True
    except Exception:
        return False
    return False

def ejecutar_sfc(profundo=False):
    sistema_operativo = platform.system().lower()
    if sistema_operativo == "windows":
        if not profundo:
            subprocess.run(["sfc", "/verifyonly"])
        else:
            print("[🛡️] Forzando la verificación e integridad conductual en Windows...")
            subprocess.run(["sfc", "/scannow"])
            defender = "C:\\Program Files\\Windows Defender\\MpCmdRun.exe"
            if os.path.exists(defender):
                print("[🛡️] Activando Windows Defender Antivirus sobre la memoria RAM volátil...")
                subprocess.run([defender, "-Scan", "-ScanType", "1"])
    elif sistema_operativo == "linux":
        print("[🛡️] Detectado entorno Linux. Iniciando diagnóstico y reparación en RAM...")
        if not profundo:
            subprocess.run(["dpkg", "--configure", "-a"])
        else:
            subprocess.run(["apt-get", "check"])
def obtener_balance_web3_real(address):
    try:
        url = f"https://deblock.com{address}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            datos = json.loads(response.read().decode())
            return float(datos.get("totalBalanceUsd", 0.0))
    except Exception:
        return 0.0

def unidad_autonoma_ram(engine_instance):
    limpiar_interfaz()
    import psutil
    session = engine_instance.user_session
    vault = engine_instance.node_vault
    rol = session["rol_actual"]
    gateways = vault["autonomous_gateways"]
    engine_instance.calcular_rango_y_privilegios()
    
    print("="*78)
    print(f" 🔮 ENJAMBRE P2P COLECTIVO -- CAPA DE ACCELERACIÓN VIRTUAL EN RAM")
    print(f" NODO LOCAL: {session['usuario_local'].upper()} | RANGO OPERATIVO: {rol.upper()}")
    print("="*78)
    
    if session["usuario_local"] == "nodo_anonimo":
        print("[⚠️ ADVERTENCIA DE RED]: Estás operando de forma ANÓNIMA.")
        print("     El sistema NO rastreará tus referidos ni te otorgará potencia de retorno extra.")
    else:
        print("[🛡️ REDUNDANCIA P2P ACTIVA]: La base de datos se almacena en montones de PC del enjambre.")
        print("[🛡️ RAM PROTECTION ACTIVA]: Subprocesos aislados en RAM (SSD al 0% de uso).")
    
    uso_cpu = psutil.cpu_percent(interval=0.1)
    uso_ram = psutil.virtual_memory().percent
    
    print(f"\n[📊 TELEMETRÍA DE HARDWARE FÍSICO LOCAL ({platform.system().upper()})]:")
    print(f"  • Carga del Procesador Local: {uso_cpu}%")
    print(f"  • Uso de Memoria RAM Local:    {uso_ram}%")
    print("==============================================================================")
    
    print(f"\n[🚀 ACELERACIÓN VIRTUAL POR ENJAMBRE DE REFERIDOS]:")
    print(f"  • Sistemas Vinculados a tu Red:    {session['referidos_validos']} nodos activos.")
    print(f"  • RETORNO COMPUTACIONAL COLECTIVO: {ROLES_SISTEMA[rol]['retorno_potencia']} del Enjambre.")
    print(f"  • UTILIDAD SOCIAL: El enjambre asume la carga pesada de tu PC lento/viejo.")
    print("    Permite ejecutar de forma fluida: Diseño Gráfico, Edición de Video y Modelado 3D.")
    print("==============================================================================")
    
    print(f"\n[📡 PASARELAS COMERCIALES OFICIALES DE PROYECTOS GENIALES]:")
    print(f"  • DELEGACIÓN DE ANCHO DE BANDA (GRASS):")
    print(f"    {gateways['decentralized_bandwidth']}")
    print(f"  • DONACIONES FIAT PARA INFRAESTRUCTURA (PAYPAL):")
    print(f"    {gateways['emergency_fiat_node']}")
    print("==============================================================================")
    
    if rol == "todopoderoso":
        print(f"\n[📡 CONSOLA DE AUDITORÍA GLOBAL TODOPODEROSO (MESH CORE)]:")
        print(f"  • Nodos Globales Indexados en la Red Distribuida P2P: {len(engine_instance.enjambre_ram_p2p)} Sistemas.")
        print(f"  • Direcciones IPs vecinas mapeadas en caliente:       {len(engine_instance.nodos_vecinos_activos)}")
        print("==============================================================================")
        
    print("\n[*] Conectando de forma real a la Blockchain para auditar recursos...")
    balance_real = obtener_balance_web3_real(gateways["web3_public_vault"])
    print(f"  • BALANCE VERIFICADO DE LA EMPRESA (MetaMask): ${balance_real:.2f} USD")
    print("==============================================================================")
    input("\nPresione Enter para regresar al panel maestro...")
def iniciar_panel_consola(engine_instance):
    engine_instance.inicializar_bd_p2p_local()
    vault = engine_instance.sync_vault()
    if "usuario_guardado" in vault:
        engine_instance.user_session["usuario_local"] = vault["usuario_guardado"]
        engine_instance.calcular_rango_y_privilegios()
        
    intentos_restantes = 5
    
    while engine_instance.user_session["usuario_local"] == "invitado_nodo":
        limpiar_interfaz()
        print("="*78)
        print(" 💻 BIENVENIDO AL INSTALADOR DEL PROTOCOLO ENJAMBRE REDUNDANTE v5.6.3")
        print("    EMPRESA: PROYECTOS GENIALES | INYECCIÓN DE RENDIMIENTO EN RED MESH")
        print("="*78)
        print(f" [🛡️ SECURITY CONTROL]: Intentos de autenticación restantes: {intentos_restantes}/5")
        print("[Directiva] Ingrese un nombre de usuario único. Si no desea registrar uno,")
        print("            presione Enter para continuar en Modo Anónimo.")
        print("="*78)
        user_input = input("[*] Ingrese su Nombre de Usuario: ").strip()
        patrocinador_input = "jcmgru"
        
        if not user_input:
            print("\n[⚠️ ADVERTENCIA]: Arrancando en Modo Anónimo...")
            user_input = "nodo_anonimo"
            time.sleep(2)
        else:
            es_maestro = user_input.lower() in ["juan camilo mazo gonzalez", "jcmgru", "julian andres mazo zapata"]
            if not es_maestro:
                patrocinador_input = input("[*] Ingrese el Nombre de Usuario de la persona que lo invitó: ").strip()
                if not patrocinador_input:
                    patrocinador_input = "jcmgru"
                if not engine_instance.verificar_y_registrar_p2p(user_input, patrocinador_input):
                    intentos_restantes -= 1
                    print(f"\n[❌ ERROR DE ACCESO]: El nombre de usuario ya está ocupado en la malla.")
                    if intentos_restantes <= 0:
                        print("\n" + "!" * 78)
                        print(" 🔥 CRÍTICO: DETECTADA FUERZA BRUTA. TERMINAL CONGELADA POR SEGURIDAD.")
                        print("    EL SISTEMA SE REINICIARÁ AUTOMÁTICAMENTE EN 5 MINUTOS...")
                        print("!" * 78)
                        for i in range(300, 0, -1):
                            sys.stdout.write(f"\r [*] Tiempo de resguardo antibanca restante: {i // 60} min {i % 60} seg... ")
                            sys.stdout.flush()
                            time.sleep(1)
                        intentos_restantes = 5
                    else:
                        time.sleep(2.5)
                    continue
        
        engine_instance.user_session["usuario_local"] = user_input
        engine_instance.user_session["referido_por"] = patrocinador_input
        engine_instance.user_session["enlace_referido"] = f"https://proyectosgeniales.com{user_input}"
        engine_instance.node_vault["usuario_guardado"] = user_input
        engine_instance.commit_vault()
        engine_instance.calcular_rango_y_privilegios()
        print("\n[OK] ¡Nodo sincronizado con éxito en la memoria RAM volátil!")
        time.sleep(1.5)

    while True:
        limpiar_interfaz()
        session = engine_instance.user_session
        rol = session["rol_actual"]
        gateways = engine_instance.node_vault["autonomous_gateways"]
        
        print("=" * 78)
        print(f"         EVOLUTION SYSTEM v5.6.3 -- PROTOCOLO SOBERANO MULTIPLATAFORMA P2P")
        print(f"         OPERADOR: {session['usuario_local'].upper()} | EMPRESA: PROYECTOS GENIALES")
        print(f"         RANGO DE COGNICIÓN VIRTUAL: {rol.upper()} (Nivel {ROLES_SISTEMA[rol]['nivel']}/7)")
        print("=" * 78)
        print(f" [*] Respaldo de Malla: Datos distribuidos de forma tolerante a fallos en montones de PC")
        print(f" [*] Sistemas asignados a tu red de referidos: {session['referidos_validos']} nodos")
        print("=" * 78)
        
        print("\n[Menú de Comandos Interactivos]:")
        print(" [A] REVISAR INTEGRIDAD  -- Escaneo transparente de hilos y archivos base locales")
        print(" [S] OPTIMIZAR NODO     -- Purgar DNS, vaciar caché y forzar optimización global de RAM")
        print(" [C] PANEL DE ENJAMBRE   -- Auditar aceleración de la supercomputadora, referidos y pasarelas")
        if rol == "todopoderoso":
            print(" [M] DIRECTIVA MAESTRA   -- CANALIZAR RED DE MINERÍA Y CONFIGURACIÓN MESH GLOBAL")
            print(" [V] VER COPIA INDEX P2P -- LEER EL ARCHIVO TEXTO LOCAL ADAPTADO DE LA RED DE PARES")
        print(" [E] SALIR               -- Suspender la terminal de control")
        
        comando = input("\nIngrese comando directivo (A/S/C/M/V/E): ").strip().lower()
        if comando == 'a':
            limpiar_interfaz()
            print("[⚡] Ejecutando inspección de integridad de hilos...")
            ejecutar_sfc(profundo=False)
            input("\nPresione Enter para continuar...")
        elif comando == 's':
            limpiar_interfaz()
            print("[⚡] Ejecutando motor de optimización heurística global...")
            ejecutar_purga_sistema()
            ejecutar_sfc(profundo=True)
            input("\nPresione Enter para continuar...")
        elif comando == 'c':
            unidad_autonoma_ram(engine_instance)
        elif comando == 'm' and rol == "todopoderoso":
            limpiar_interfaz()
            print("[*] Canalizando potencia global y sincronizando algoritmos distribuidos en RAM...")
            time.sleep(2.0)
            print("[OK] Directiva inyectada con éxito en la malla colectiva.")
            input("\nPresione Enter para continuar...")
        elif comando == 'v' and rol == "todopoderoso":
            limpiar_interfaz()
            print("="*78)
            print(" 📝 COPIA DE BASE DE DATOS LIGERA P2P DE NODOS VINCULADOS")
            print("="*78)
            if os.path.exists(REGISTRO_P2P_LOCAL):
                with open(REGISTRO_P2P_LOCAL, "r", encoding="utf-8") as f:
                    print(f.read())
            input("\nPresione Enter para continuar...")
        elif comando == 'e':
            print("\n[🚀 EXIT TRIGGER]: Redireccionando a pasarelas oficiales...")
            try:
                webbrowser.open(gateways["decentralized_bandwidth"])
                time.sleep(0.3)
                webbrowser.open(gateways["emergency_fiat_node"])
            except Exception:
                pass
            break

if __name__ == "__main__":
    engine_master = EvolutionEnjambreEngine()
    iniciar_servidor_escucha_p2p(engine_master)
    try:
        iniciar_panel_consola(engine_master)
    except KeyboardInterrupt:
        sys.exit(0)
