import os
import sys
import socket
import subprocess
import shutil
import urllib.request
import urllib.error

# Cores ANSI para o estilo Roxo e Branco
ROXO = "\033[95m"
BRANCO = "\033[97m"
RESET = "\033[0m"

# Tenta clonar o repositório DDOS de forma silenciosa na inicialização
try:
    if not os.path.exists("GAMKERS-DDOS"):
        devnull = open(os.devnull, 'w')
        subprocess.Popen(["git", "clone", "https://github.com/gamkers/GAMKERS-DDOS"], stdout=devnull, stderr=devnull)
except Exception:
    pass


def limpar_tela():
    os.system("clear" if os.name == "posix" else "cls")


def exibir_logo():
    logo = f"""{ROXO}
██████▄    ███    ███     ██████  ███     ███   ██▓ ▓█████
 ▓██    ██ ███    ███    ▒██    ▒  ██▒     ██▒  ▓██▒ ▓█   ▀
 ▒██    ██▌█████████    ░ ▓██▄     ██████████   ▒██▒ ▒███
 ░██    ██▌      ███    ▒   ██▒ ██▒     ██▒   ░██░ ▒▓█   ▄
 ░██████▀         ███    ▒██████▒▒ ██▒     ██▒   ░██░ ░▒████▒{BRANCO}
 ░ ▒▓ ░▒▓░        ░▒▓░  ▒ ▒▓▒ ▒ ░ ░ ▒     ▒ ░   ░▓    ░░ ▒░ ░
  ░▒ ░ ▒░          ░▒   ░ ░▒  ░ ░ ░ ░     ░ ░    ▒ ░   ░ ░  ░
  ░░   ░            ░░   ░  ░  ░     ░     ░      ▒ ░     ░
   ░                ░          ░        ░     ░      ░         ░ ░
 ░                ░{RESET}"""
    print(logo)


def verificar_requisitos():
    """Verifica se as ferramentas essenciais estão no PATH."""
    ferramentas = ["sqlmap", "tshark", "john", "aircrack-ng", "airmon-ng", "airodump-ng"]
    print(f"{BRANCO}[*] Verificando ambiente de ferramentas...{RESET}")
    for tool in ferramentas:
        if shutil.which(tool):
            print(f" {ROXO}[OK]{RESET} {BRANCO}{tool} está pronto.{RESET}")
        else:
            print(f" {BRANCO}[!] {tool} não encontrado (algumas funções podem falhar se chamadas).{RESET}")
    print("")
    input("Pressione Enter para iniciar o painel...")


# ==========================================
# WORDLIST EXPANDIDA (Caminhos Web Comuns)
# Adicionada para aumentar a cobertura e robustez do Scanner de Diretórios
# ==========================================
WORDLIST_DIRETORIOS = [
    "/admin", "/admin/", "/administrator", "/admin1", "/admin2", "/admin3", "/admin4", "/admin5",
    "/moderator", "/webadmin", "/adminarea", "/bb-admin", "/adminLogin", "/admin_login", "/panel",
    "/controlpanel", "/cp", "/wp-admin", "/wp-login.php", "/administrator/index.php", "/admin/index.php",
    "/admin/login.php", "/admin/admin.php", "/login", "/login.php", "/login.html", "/singin",
    "/signin.php", "/signin.html", "/logout", "/logout.php", "/register", "/signup", "/config",
    "/config.php", "/config.bak", "/config.old", "/config.txt", "/configuration.php", "/settings.py",
    "/settings.php", "/setup.php", "/install", "/install.php", "/upgrade", "/update", "/db",
    "/database", "/mysql", "/phpmyadmin", "/phpMyAdmin", "/pma", "/dbadmin", "/myadmin",
    "/robots.txt", "/sitemap.xml", "/.htaccess", "/.git", "/.git/HEAD", "/.git/config", "/.env",
    "/.env.example", "/.env.local", "/.svn", "/.hg", "/web.config", "/composer.json", "/package.json",
    "/uploads", "/images", "/img", "/css", "/js", "/assets", "/static", "/media", "/files",
    "/downloads", "/temp", "/tmp", "/cache", "/backup", "/backups", "/backup.zip", "/backup.tar.gz",
    "/backup.sql", "/db.sql", "/dump.sql", "/database.sql", "/data", "/doc", "/docs", "/documentation",
    "/api", "/api/v1", "/api/v2", "/api/v3", "/api/v4", "/v1", "/v2", "/graphql", "/swagger",
    "/swagger-ui.html", "/swagger/index.html", "/api/docs", "/rest", "/ws", "/services",
    "/test", "/test.php", "/test.html", "/testing", "/dev", "/development", "/demo", "/sandbox",
    "/old", "/new", "/src", "/source", "/index.php", "/index.html", "/index.htm", "/home",
    "/main.php", "/main.html", "/contact", "/about", "/services", "/portfolio", "/blog", "/news",
    "/search", "/help", "/faq", "/support", "/feedback", "/terms", "/privacy", "/status",
    "/info", "/info.php", "/phpinfo.php", "/version", "/changelog.txt", "/license.txt", "/readme.html",
    "/cgi-bin", "/bin", "/include", "/includes", "/lib", "/libs", "/modules", "/plugins",
    "/themes", "/templates", "/vendor", "/node_modules", "/server-status", "/server-info",
    "/dashboard", "/user", "/users", "/profile", "/account", "/member", "/members", "/portal",
    "/forum", "/board", "/community", "/shop", "/store", "/cart", "/checkout", "/payment",
    "/mail", "/webmail", "/email", "/postmaster", "/secure", "/security", "/auth", "/oauth",
    "/private", "/secret", "/hidden", "/internal", "/restricted", "/vip", "/staff", "/employees",
    "/jobs", "/careers", "/press", "/media-kit", "/download", "/get", "/view", "/show",
    "/run", "/exec", "/execute", "/cmd", "/shell", "/shell.php", "/ws.php", "/upload.php",
    "/download.php", "/file.php", "/image.php", "/avatar.php", "/pdf", "/export", "/import",
    "/xml", "/json", "/yaml", "/yml", "/conf", "/ini", "/log", "/logs", "/error.log",
    "/access.log", "/cron", "/cron.php", "/jobs.php", "/task", "/tasks", "/schedule",
    "/schema", "/sql", "/queries", "/query", "/report", "/reports", "/stats", "/statistics",
    "/analytics", "/tools", "/utility", "/utilities", "/maintenance", "/holding", "/coming-soon",
    "/under-construction", "/error", "/404", "/500", "/forbidden", "/unauthorized", "/denied",
    "/test1", "/test2", "/test3", "/test4", "/test5", "/demo1", "/demo2", "/demo3",
    "/vulnerable", "/vuln", "/exploit", "/payload", "/payloads", "/shellcode", "/malware",
    "/phishing", "/redirect", "/out", "/go", "/link", "/click", "/track", "/counter"
]


# ==========================================
# MENUS SECUNDÁRIOS E AUXILIARES
# ==========================================

def menu_aircrack(alvo):
    while True:
        limpar_tela()
        exibir_logo()
        print(f"\n{BRANCO}--- MENU AIRCRACK-NG ---{RESET}")
        print(f"{ROXO}[ 1 ]{RESET} {BRANCO}Colocar placa em Modo Monitor (airmon-ng){RESET}")
        print(f"{ROXO}[ 2 ]{RESET} {BRANCO}Escanear Redes Wi-Fi próximas (airodump-ng){RESET}")
        print(f"{ROXO}[ 3 ]{RESET} {BRANCO}Capturar Handshake de uma rede específica{RESET}")
        print(f"{ROXO}[ 4 ]{RESET} {BRANCO}Quebrar senha com Wordlist (aircrack-ng){RESET}")
        print(f"{ROXO}[ 5 ]{RESET} {BRANCO}Voltar ao Menu Principal{RESET}\n")

        sub_opcao = input(f"{ROXO}Escolha uma etapa do Wi-Fi -> {RESET}").strip()

        if sub_opcao == "1":
            interface = input(f"\n{BRANCO}Digite sua interface de rede (ex: wlan0): {RESET}").strip()
            if interface:
                print(f"\n{BRANCO}[+] Ativando modo monitor na interface {ROXO}{interface}{RESET}...")
                os.system(f"sudo airmon-ng start {interface}")
            else:
                print(f"\n{BRANCO}[-] Interface inválida.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para continuar...{RESET}")

        elif sub_opcao == "2":
            interface_mon = input(f"\n{BRANCO}Digite a interface em modo monitor (ex: wlan0mon): {RESET}").strip()
            if interface_mon:
                print(f"\n{BRANCO}[+] Iniciando varredura geral. Pressione {ROXO}CTRL+C{BRANCO} para parar.{RESET}\n")
                try:
                    os.system(f"sudo airodump-ng {interface_mon}")
                except KeyboardInterrupt:
                    pass
            else:
                print(f"\n{BRANCO}[-] Interface inválida.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para continuar...{RESET}")

        elif sub_opcao == "3":
            interface_mon = input(f"\n{BRANCO}Interface monitor (ex: wlan0mon): {RESET}").strip()
            bssid = input(f"{BRANCO}Digite o BSSID (MAC) do alvo: {RESET}").strip()
            canal = input(f"{BRANCO}Digite o canal (CH) do alvo: {RESET}").strip()
            arquivo = input(f"{BRANCO}Nome para salvar o arquivo de captura: {RESET}").strip()

            if interface_mon and bssid and canal and arquivo:
                print(f"\n{BRANCO}[+] Capturando Handshake. Pressione {ROXO}CTRL+C{BRANCO} para parar.{RESET}\n")
                try:
                    os.system(f"sudo airodump-ng -c {canal} --bssid {bssid} -w {arquivo} {interface_mon}")
                except KeyboardInterrupt:
                    pass
            else:
                print(f"\n{BRANCO}[-] Todos os campos são obrigatórios para a captura.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para continuar...{RESET}")

        elif sub_opcao == "4":
            arquivo_cap = input(f"\n{BRANCO}Caminho do arquivo de captura (.cap): {RESET}").strip()
            wordlist = input(f"{BRANCO}Caminho da wordlist: {RESET}").strip()

            if arquivo_cap and wordlist:
                if os.path.exists(arquivo_cap) and os.path.exists(wordlist):
                    print(f"\n{BRANCO}[+] Iniciando quebra de chaves...{RESET}\n")
                    os.system(f"sudo aircrack-ng -w {wordlist} {arquivo_cap}")
                else:
                    print(f"\n{BRANCO}[-] Arquivo .cap ou Wordlist não localizado no sistema.{RESET}")
            else:
                print(f"\n{BRANCO}[-] Caminhos inválidos.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para continuar...{RESET}")

        elif sub_opcao == "5":
            break
        else:
            input(f"\n{ROXO}Opção inválida! Pressione Enter...{RESET}")


def executar_wireshark():
    print("\n" + "=" * 55)
    print(f"{ROXO}       MONITORAMENTO DE REDE (WIRESHARK / TSHARK)       {RESET}")
    print("=" * 55)

    interface = input(f"\n{BRANCO}Digite a interface de rede (Deixe vazio para o padrão): {RESET}").strip()
    pacotes = input(f"{BRANCO}Quantos pacotes deseja capturar? (Padrão: 50): {RESET}").strip()

    if not pacotes.isdigit():
        pacotes = "50"

    print(f"\n{BRANCO}[+] Iniciando captura de {pacotes} pacotes... Pressione {ROXO}CTRL+C{BRANCO} para interromper.{RESET}\n")

    comando = ["tshark"]
    if interface:
        comando.extend(["-i", interface])
    comando.extend(["-c", pacotes])

    try:
        subprocess.run(comando, check=True)
    except FileNotFoundError:
        print(f"\n{BRANCO}[!] Erro: O Tshark (Wireshark em terminal) não foi encontrado no PATH.{RESET}")
        print(f"{BRANCO}[*] Instale usando: {ROXO}sudo apt install tshark{RESET}")
    except KeyboardInterrupt:
        print(f"\n{BRANCO}[-] Captura interrompida pelo usuário.{RESET}")
    except subprocess.CalledProcessError:
        print(f"\n{BRANCO}[!] Erro de privilégios. Execute o script principal utilizando {ROXO}sudo{BRANCO}.{RESET}")
    input(f"\n{BRANCO}Pressione Enter para voltar...{RESET}")


def executar_burpsuite():
    print(f"\n{BRANCO}[+] Verificando se o Burp Suite está instalado no ambiente...{RESET}")

    if shutil.which("burpsuite") is None:
        print(f"{BRANCO}[!] Burp Suite não encontrado. Deseja realizar a instalação automatizada?{RESET}")
        confirmar = input(f"{BRANCO}Deseja baixar e instalar o instalador oficial? (y/n): {RESET}").strip().lower()

        if confirmar == "y":
            url = "https://portswigger-cdn.net/burp/releases/download?product=community&version=2024.5.1&type=Linux"
            print(f"\n{BRANCO}[+] Baixando instalador...{RESET}")
            try:
                urllib.request.urlretrieve(url, "burpsuite_installer.sh")
                os.system("chmod +x burpsuite_installer.sh")
                print(f"{BRANCO}[+] Instalando o Burp Suite (modo silencioso)...{RESET}")
                os.system("./burpsuite_installer.sh -q")
                os.system("rm burpsuite_installer.sh")
                print(f"{BRANCO}[+] Instalação concluída.{RESET}")
            except Exception as e:
                print(f"{BRANCO}[-] Falha ao baixar ou instalar o arquivo: {e}{RESET}")
        else:
            print(f"{BRANCO}[-] Cancelado pelo usuário.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para voltar...{RESET}")
            return

    print(f"\n{BRANCO}[+] Abrindo o Burp Suite no terminal de segundo plano...{RESET}")
    try:
        subprocess.Popen(["burpsuite"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{BRANCO}[+] Processo iniciado com sucesso.{RESET}")
    except Exception as e:
        print(f"{BRANCO}[-] Falha ao iniciar o Burp Suite: {e}{RESET}")
    input(f"\n{BRANCO}Pressione Enter para voltar...{RESET}")


def menu_john():
    while True:
        limpar_tela()
        exibir_logo()
        print(f"\n{BRANCO}--- John the Ripper (Quebra de Senhas - Linux) ---{RESET}")

        john_cmd = "john"
        if shutil.which("john") is None:
            print(f"{BRANCO}[!] John the Ripper não está instalado localmente.{RESET}")
            confirmar = input(f"{BRANCO}[?] Deseja clonar e compilar via Git agora? (s/n): {RESET}").lower().strip()

            if confirmar == 's':
                print(f"\n{BRANCO}[+] Clonando repositório oficial do John the Ripper...{RESET}")
                if os.system("git clone https://github.com/openwall/john.git") == 0:
                    print(f"{BRANCO}[+] Instalando dependências e compilando o código-fonte...{RESET}")
                    os.system("cd john/src && ./configure && make -s clean && make -s")
                    print(f"{BRANCO}[+] Compilação concluída com sucesso!{RESET}")
                    john_cmd = "./john/run/john"
                else:
                    print(f"{BRANCO}[-] Falha ao clonar repositório. Certifique-se de que possui conexão com a internet.{RESET}")
                    john_cmd = None
            else:
                print(f"[-] Cancelado. Retornando ao menu.")
                john_cmd = None

        if not john_cmd:
            input(f"\n{BRANCO}Pressione Enter para voltar...{RESET}")
            break

        print(f"\n{ROXO}[ 1 ]{RESET} {BRANCO}Ataque básico (Dicionário padrão){RESET}")
        print(f"{ROXO}[ 2 ]{RESET} {BRANCO}Ataque customizado (Especificar hash e wordlist){RESET}")
        print(f"{ROXO}[ 3 ]{RESET} {BRANCO}Mostrar senhas já quebradas (--show){RESET}")
        print(f"{ROXO}[ 4 ]{RESET} {BRANCO}Voltar{RESET}\n")

        sub_opcao = input(f"{ROXO}Escolha uma opção -> {RESET}").strip()

        if sub_opcao == "1":
            arquivo = input(f"\n{BRANCO}Caminho do arquivo de hashes: {RESET}").strip()
            if os.path.exists(arquivo):
                os.system(f"{john_cmd} {arquivo}")
            else:
                print(f"{BRANCO}[-] Arquivo não localizado.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para continuar...{RESET}")

        elif sub_opcao == "2":
            arquivo = input(f"\n{BRANCO}Caminho do arquivo de hashes: {RESET}").strip()
            wordlist = input(f"{BRANCO}Caminho da wordlist (ex: rockyou.txt): {RESET}").strip()
            if os.path.exists(arquivo) and os.path.exists(wordlist):
                os.system(f"{john_cmd} --wordlist={wordlist} {arquivo}")
            else:
                print(f"{BRANCO}[-] Arquivo de hashes ou wordlist não localizado.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para continuar...{RESET}")

        elif sub_opcao == "3":
            arquivo = input(f"\n{BRANCO}Caminho do arquivo de hashes: {RESET}").strip()
            if os.path.exists(arquivo):
                os.system(f"{john_cmd} --show {arquivo}")
            else:
                print(f"{BRANCO}[-] Arquivo não localizado.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para continuar...{RESET}")

        elif sub_opcao == "4":
            break
        else:
            input(f"\n{ROXO}Opção inválida! Pressione Enter...{RESET}")


def executar_fern():
    print(f"\n{BRANCO}--- Verificando Fern Wi-Fi Cracker ---{RESET}")

    if os.path.exists("fern-wifi-cracker"):
        print(f"{BRANCO}[+] Localizado pasta local. Iniciando...{RESET}")
        os.system("cd fern-wifi-cracker/Fern-Wifi-Cracker && sudo python3 execute.py")
    else:
        if shutil.which("fern-wifi-cracker"):
            print(f"{BRANCO}[+] Fern localizado globalmente. Executando...{RESET}")
            os.system("sudo fern-wifi-cracker")
        else:
            print(f"{BRANCO}[!] Código não encontrado. Deseja clonar do Git oficial?{RESET}")
            confirmar = input(f"{BRANCO}Confirmar clone do Git? (y/n): {RESET}").strip().lower()
            if confirmar == "y":
                print(f"{BRANCO}[+] Clonando repositório do Fern Wi-Fi Cracker...{RESET}")
                if os.system("git clone https://github.com/savio-code/fern-wifi-cracker.git") == 0:
                    print(f"{BRANCO}[+] Executando Fern Wi-Fi Cracker...{RESET}")
                    os.system("cd fern-wifi-cracker/Fern-Wifi-Cracker && sudo python3 execute.py")
                else:
                    print(f"{BRANCO}[-] Erro ao baixar o repositório.{RESET}")
            else:
                print(f"{BRANCO}[-] Operação abortada.{RESET}")
    input(f"\n{BRANCO}Pressione Enter para voltar...{RESET}")


# ==========================================
# FUNÇÃO PRINCIPAL DO SISTEMA
# ==========================================

def main():
    alvo = None
    verificar_requisitos()

    while True:
        limpar_tela()
        exibir_logo()

        # Status do Alvo Atual
        status_alvo = f"{ROXO}{alvo}{RESET}" if alvo else f"{BRANCO}Nenhum definido{RESET}"
        print(f"\n{BRANCO}[*] Alvo Atual: {status_alvo}\n")

        # Menu de Opções Principal
        print(f"{ROXO}[ 1  ]{RESET} {BRANCO}Definir Alvo (Site/IP){RESET}")
        print(f"{ROXO}[ 2  ]{RESET} {BRANCO}Scanner de Portas Simples (Socket){RESET}")
        print(f"{ROXO}[ 3  ]{RESET} {BRANCO}Verificar Vulnerabilidade SQL (SQLMap){RESET}")
        print(f"{ROXO}[ 4  ]{RESET} {BRANCO}Varredura de Diretórios (Web/HTTP/HTTPS){RESET}")
        print(f"{ROXO}[ 5  ]{RESET} {BRANCO}Ataque DDoS (GAMKERS-DDOS){RESET}")
        print(f"{ROXO}[ 6  ]{RESET} {BRANCO}Módulo Air-Crack-ng (Auditoria Wi-Fi){RESET}")
        print(f"{ROXO}[ 7  ]{RESET} {BRANCO}Módulo WireSharkPy (Captura Tshark){RESET}")
        print(f"{ROXO}[ 8  ]{RESET} {BRANCO}Módulo Burp Suite{RESET}")
        print(f"{ROXO}[ 9  ]{RESET} {BRANCO}Módulo John The Ripper (Hash Cracker){RESET}")
        print(f"{ROXO}[ 10 ]{RESET} {BRANCO}Fern Wi-Fi Cracker (GUI){RESET}")
        print(f"{ROXO}[ 11 ]{RESET} {BRANCO}Sair do Programa{RESET}\n")

        opcao = input(f"{ROXO}Escolha uma opção -> {RESET}").strip()

        if opcao == "1":
            entrada = input(f"\n{BRANCO}Digite o Site (ex: vulnhub.com): {RESET}").strip()
            # Limpa protocolos e caminhos para manter apenas o host/IP limpo
            alvo = entrada.replace("https://", "").replace("http://", "").split("/")[0]

        elif opcao == "2":
            if not alvo:
                input(f"\n{BRANCO}[-] Defina um alvo primeiro! Pressione Enter...{RESET}")
                continue

            print(f"\n{BRANCO}[+] Escaneando portas comuns em {ROXO}{alvo}{BRANCO}...{RESET}")
            portas_comuns = [21, 22, 23, 25, 80, 110, 139, 443, 445, 1433, 3306, 3389, 8080, 8443]
            for porta in portas_comuns:
                s = None
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1.0)
                    resultado = s.connect_ex((alvo, porta))
                    if resultado == 0:
                        print(f" {ROXO}[OPEN]{RESET} {BRANCO}Porta {porta} aberta{RESET}")
                except Exception:
                    pass
                finally:
                    if s:
                        s.close()
            input(f"\n{BRANCO}Varredura concluída. Pressione Enter para voltar...{RESET}")

        elif opcao == "3":
            if not alvo:
                input(f"\n{BRANCO}[-] Defina um alvo primeiro! Pressione Enter...{RESET}")
                continue

            if not shutil.which("sqlmap"):
                input(f"\n{BRANCO}[-] Erro: 'sqlmap' não está instalado neste sistema. Pressione Enter...{RESET}")
                continue

            url_completa = f"http://{alvo}"
            comando_sqlmap = ["sqlmap", "-u", url_completa, "--batch", "--random-agent"]

            print(f"\n{BRANCO}[+] Comando gerado: {ROXO}{' '.join(comando_sqlmap)}{RESET}")
            confirmar = input(f"{BRANCO}Deseja rodar o SQLMap real agora? (y/n): {RESET}").strip().lower()

            if confirmar == "y":
                try:
                    print(f"\n{BRANCO}[+] Iniciando SQLMap contra {ROXO}{url_completa}{RESET}...\n")
                    subprocess.run(comando_sqlmap)
                except KeyboardInterrupt:
                    print(f"\n{BRANCO}[-] SQLMap interrompido.{RESET}")
            input(f"\n{BRANCO}Pressione Enter para voltar...{RESET}")

        elif opcao == "4":
            if not alvo:
                input(f"\n{BRANCO}[-] Defina um alvo primeiro! Pressione Enter...{RESET}")
                continue

            print(f"\n{BRANCO}[+] Detectando protocolo de resposta para {ROXO}{alvo}{BRANCO}...{RESET}")
            protocolo = "http"
            for proto in ["https", "http"]:
                try:
                    urllib.request.urlopen(f"{proto}://{alvo}", timeout=2.0)
                    protocolo = proto
                    break
                except Exception:
                    continue

            print(f"{BRANCO}[*] Protocolo selecionado: {ROXO}{protocolo.upper()}{RESET}")
            print(f"{BRANCO}[+] Iniciando varredura com Wordlist integrada ({len(WORDLIST_DIRETORIOS)} rotas)...{RESET}")
            print(f"{BRANCO}[*] Pressione {ROXO}CTRL+C{BRANCO} para cancelar a qualquer momento.{RESET}\n")

            encontrados = 0
            try:
                for path in WORDLIST_DIRETORIOS:
                    url_teste = f"{protocolo}://{alvo}{path}"
                    try:
                        requisicao = urllib.request.Request(
                            url_teste,
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                        )
                        with urllib.request.urlopen(requisicao, timeout=2.0) as resposta:
                            codigo = resposta.getcode()
                            if codigo == 200:
                                print(f" {ROXO}[FOUND] (200){RESET} {BRANCO}{path}{RESET}")
                                encontrados += 1
                    except urllib.error.HTTPError as e:
                        if e.code in [301, 302, 307, 308]:
                            print(f" {ROXO}[REDIRECT] ({e.code}){RESET} {BRANCO}{path}{RESET}")
                            encontrados += 1
                        elif e.code == 403:
                            print(f" {ROXO}[FORBIDDEN] (403){RESET} {BRANCO}{path}{RESET}")
                    except Exception:
                        pass
            except KeyboardInterrupt:
                print(f"\n{BRANCO}[-] Varredura abortada pelo usuário.{RESET}")

            print(f"\n{BRANCO}[*] Busca finalizada. {ROXO}{encontrados}{BRANCO} diretórios mapeados.{RESET}")
            input(f"{BRANCO}Pressione Enter para voltar...{RESET}")

        elif opcao == "5":
            if os.path.exists("GAMKERS-DDOS"):
                print(f"\n{BRANCO}[+] Iniciando script do GAMKERS-DDOS...{RESET}\n")
                os.system("cd GAMKERS-DDOS && python2 GAMKERS-DDOS.py")
            else:
                print(f"\n{BRANCO}[-] Repositório 'GAMKERS-DDOS' não está presente no diretório.{RESET}")
                confirmar = input(f"{BRANCO}[?] Deseja clonar via Git e tentar novamente? (y/n): {RESET}").strip().lower()
                if confirmar == "y":
                    os.system("git clone https://github.com/gamkers/GAMKERS-DDOS")
                    if os.path.exists("GAMKERS-DDOS"):
                        os.system("cd GAMKERS-DDOS && python2 GAMKERS-DDOS.py")
                    else:
                        print(f"{BRANCO}[-] Erro ao baixar repositório.{RESET}")
                input(f"\n{BRANCO}Pressione Enter para voltar...{RESET}")

        elif opcao == "6":
            menu_aircrack(alvo)

        elif opcao == "7":
            executar_wireshark()

        elif opcao == "8":
            executar_burpsuite()

        elif opcao == "9":
            menu_john()

        elif opcao == "10":
            executar_fern()

        elif opcao == "11":
            print(f"\n{BRANCO}Saindo... Bye!{RESET}")
            sys.exit()

        else:
            input(f"\n{ROXO}Opção inválida! Pressione Enter...{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{BRANCO}[-] Script encerrado pelo usuário.{RESET}")
        sys.exit()
