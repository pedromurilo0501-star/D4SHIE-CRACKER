#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
          PENTEST ALL-IN-ONE SYSTEM PANEL & AUTOMATIC INSTALLER v4.0
================================================================================
Desenvolvido para CachyOS (KDE Plasma / Konsole).
Instala dependências via Pacman, clona repositórios e corrige sintaxe antiga.
================================================================================
"""

import os
import sys
import time
import socket
import re
import subprocess
import shutil
import urllib.request
import urllib.error
from datetime import datetime

# ==========================================
# CONSTANTES DE DESIGN E CORES (Estilo Roxo)
# ==========================================
ROXO = "\033[95m"
BRANCO = "\033[97m"
CINZA = "\033[90m"
VERMELHO = "\033[91m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
RESET = "\033[0m"

# Wordlist embutida para o Fuzzer de Diretórios
WORDLIST_DIRETORIOS = [
    "/admin", "/administrator", "/wp-admin", "/wp-login.php", "/login", "/login.php",
    "/config.php", "/.env", "/.git", "/robots.txt", "/phpmyadmin", "/api", "/uploads",
    "/shell.php", "/backup.zip", "/setup.php", "/db.sql", "/server-status"
]

def limpar_tela():
    os.system("clear" if os.name == "posix" else "cls")

def exibir_logo():
    logo = f"""{ROXO}
██████▄    ███    ███     ██████  ███     ███   ██▓ ▓█████
 ▓██    ██ ███    ███    ▒██    ▒  ██▒     ██▒  ▓██▒ ▓█   ▀
 ▒██    ██▌█████████    ░ ▓██▄     ██████████   ▒██▒ ▒███
 ░██    ██▌      ███    ▒   ██▒ ██▒     ██▒   ░██░ ▒▓█   ▄
 ░██████▀         ███    ▒██████▒▒ ██▒     ██▒   ░██░ ░▒████▒{BRANCO}
       INSTALADOR E PAINEL AUTOMÁTICO - CACHYOS EDITION{RESET}"""
    print(logo)

def log_mensagem(tipo, mensagem):
    agora = datetime.now().strftime("%H:%M:%S")
    prefixo = f"{CINZA}[{agora}]{RESET} "
    if tipo == "info":
        print(f"{prefixo}{BRANCO}[*] {mensagem}{RESET}")
    elif tipo == "sucesso":
        print(f"{prefixo}{VERDE}[+] {mensagem}{RESET}")
    elif tipo == "aviso":
        print(f"{prefixo}{AMARELO}[!] {mensagem}{RESET}")
    elif tipo == "erro":
        print(f"{prefixo}{VERMELHO}[-]{RESET} {VERMELHO}{mensagem}{RESET}")

def abrir_em_nova_aba(comando, titulo="Terminal"):
    """Força abertura em nova aba no Konsole do KDE."""
    if shutil.which("konsole"):
        cmd_completo = [
            "konsole", "--new-tab", 
            "-p", f"tabtitle={titulo}", 
            "-e", "bash", "-c", 
            f"{comando}; echo; read -p 'Processo finalizado. Pressione Enter para sair...'"
        ]
        subprocess.Popen(cmd_completo)
        log_mensagem("sucesso", f"Janela '{titulo}' aberta em nova aba do Konsole.")
    else:
        log_mensagem("aviso", "Konsole não detectado. Executando localmente...")
        os.system(comando)

# ==========================================
# CLASSE: INSTALADOR E GERENCIADOR DE REQUISITOS
# ==========================================
class InstaladorCachyOS:
    def __init__(self):
        # Mapeamento de binários para pacotes do Arch/CachyOS
        self.pacotes_pacman = {
            "sqlmap": "sqlmap",
            "tshark": "wireshark-cli",
            "john": "john",
            "aircrack-ng": "aircrack-ng",
            "wireshark-qt": "wireshark-qt",
            "git": "git",
            "python-pip": "python-pip"
        }

    def instalar_tudo(self):
        limpar_tela()
        exibir_logo()
        log_mensagem("info", "Iniciando instalação de ferramentas do sistema via pacman...")
        
        # Sincroniza e instala todos de uma vez só para poupar tempo
        lista_instalar = []
        for binario, pacote in self.pacotes_pacman.items():
            if not shutil.which(binario):
                lista_instalar.append(pacote)
        
        if lista_instalar:
            comando_pacman = f"sudo pacman -S --noconfirm --needed {' '.join(lista_instalar)}"
            log_mensagem("info", f"Executando: {comando_pacman}")
            retorno = os.system(comando_pacman)
            if retorno == 0:
                log_mensagem("sucesso", "Todos os pacotes pacman foram instalados com sucesso!")
            else:
                log_mensagem("erro", "Ocorreu uma falha ao executar o Pacman. Verifique se digitou o sudo corretamente.")
        else:
            log_mensagem("sucesso", "Todas as ferramentas básicas do sistema já estão instaladas.")

        # Clonar e configurar repositórios adicionais
        self.configurar_repositorios()
        input(f"\n{BRANCO}Configuração concluída. Pressione Enter para abrir o menu do painel...{RESET}")

    def configurar_repositorios(self):
        # 1. GAMKERS-DDOS
        if not os.path.exists("GAMKERS-DDOS"):
            log_mensagem("info", "Clonando repositório GAMKERS-DDOS...")
            os.system("git clone https://github.com/gamkers/GAMKERS-DDOS")
        else:
            log_mensagem("sucesso", "Repositório GAMKERS-DDOS já existe localmente.")

        self.corrigir_sintaxe_python3("GAMKERS-DDOS/GAMKERS-DDOS.py")

        # 2. Fern Wi-Fi Cracker
        if not os.path.exists("fern-wifi-cracker"):
            log_mensagem("info", "Clonando repositório Fern Wi-Fi Cracker...")
            os.system("git clone https://github.com/savio-code/fern-wifi-cracker.git")
        else:
            log_mensagem("sucesso", "Repositório Fern Wi-Fi Cracker já existe.")

    def corrigir_sintaxe_python3(self, caminho_arquivo):
        """Converte automaticamente instruções print de Python 2 para Python 3."""
        if not os.path.exists(caminho_arquivo):
            log_mensagem("erro", f"Arquivo {caminho_arquivo} para patch de compatibilidade não foi encontrado.")
            return

        log_mensagem("info", f"Aplicando patch de conversão de Python 2 para Python 3 em: {caminho_arquivo}")
        try:
            with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
                linhas = f.readlines()

            novas_linhas = []
            regex_print = re.compile(r"^(\s*print)\s+[\"'](.*?)[\"'](.*)$")
            regex_print_var = re.compile(r"^(\s*print)\s+([a-zA-Z_][a-zA-Z0-9_]*.*?)$")

            for linha in linhas:
                # Trata prints de strings simples: print "texto" -> print("texto")
                match = regex_print.match(linha)
                if match:
                    indentacao_e_print = match.group(1)
                    conteudo = match.group(2)
                    resto = match.group(3)
                    linha_corrigida = f"{indentacao_e_print}(\"{conteudo}\"){resto}\n"
                    novas_linhas.append(linha_corrigida)
                    continue

                # Trata prints de variáveis ou chamadas compostas que não usam parênteses
                match_var = regex_print_var.match(linha)
                if match_var and not match_var.group(2).strip().startswith("("):
                    indentacao_e_print = match_var.group(1)
                    conteudo = match_var.group(2).strip()
                    linha_corrigida = f"{indentacao_e_print}({conteudo})\n"
                    novas_linhas.append(linha_corrigida)
                    continue

                novas_linhas.append(linha)

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.writelines(novas_linhas)

            log_mensagem("sucesso", "Patch de sintaxe aplicado com sucesso! Pronto para rodar no Python 3.")
        except Exception as e:
            log_mensagem("erro", f"Erro ao aplicar patch automático: {e}")

# ==========================================
# CLASSES DE RECURSOS DO PAINEL
# ==========================================

class PortScanner:
    def __init__(self, alvo):
        self.alvo = alvo
        self.portas_comuns = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]

    def rodar(self):
        if not self.alvo:
            log_mensagem("erro", "Defina um alvo no menu principal primeiro.")
            input("\nPressione Enter para continuar...")
            return
        limpar_tela()
        exibir_logo()
        log_mensagem("info", f"Verificando portas abertas em: {self.alvo}")
        try:
            ip = socket.gethostbyname(self.alvo)
            print(f"IP do Alvo: {ip}\n" + "-"*40)
            for porta in self.portas_comuns:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                resultado = sock.connect_ex((ip, porta))
                if resultado == 0:
                    print(f" {VERDE}[ABERTA]{RESET} Porta {porta:<5} | TCP")
                sock.close()
        except Exception as e:
            log_mensagem("erro", f"Erro ao escanear: {e}")
        input(f"\n{BRANCO}Pressione Enter para continuar...{RESET}")

class WebFuzzer:
    def __init__(self, alvo):
        self.alvo = alvo

    def rodar(self):
        if not self.alvo:
            log_mensagem("erro", "Defina um alvo no menu principal primeiro.")
            input("\nPressione Enter para continuar...")
            return
        limpar_tela()
        exibir_logo()
        log_mensagem("info", f"Varrendo caminhos em: http://{self.alvo}")
        print("-"*50)
        for rota in WORDLIST_DIRETORIOS:
            url = f"http://{self.alvo}{rota}"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=1.5) as res:
                    if res.getcode() == 200:
                        print(f" {VERDE}[200]{RESET} Encontrado: {url}")
            except urllib.error.HTTPError as e:
                if e.code in [301, 302, 403]:
                    print(f" {AZUL}[{e.code}]{RESET} Restrito/Redirecionado: {url}")
            except Exception:
                pass
        print("-"*50)
        input(f"\n{BRANCO}Fuzzing finalizado. Pressione Enter para continuar...{RESET}")

# ==========================================
# LOOP PRINCIPAL
# ==========================================
def main():
    alvo = None
    instalador = InstaladorCachyOS()

    # Executa a instalação de tudo na primeira inicialização
    instalador.instalar_tudo()

    while True:
        limpar_tela()
        exibir_logo()

        status_alvo = f"{ROXO}{alvo}{RESET}" if alvo else f"{VERMELHO}Nenhum Alvo Definido{RESET}"
        print(f" Alvo Ativo: {status_alvo}")
        print(" " + "=" * 50 + "\n")

        print(f" {ROXO}[ 1  ]{RESET} {BRANCO}Definir Novo Alvo{RESET}")
        print(f" {ROXO}[ 2  ]{RESET} {BRANCO}Scanner de Portas TCP Sockets{RESET}")
        print(f" {ROXO}[ 3  ]{RESET} {BRANCO}Fuzzing de Diretórios Web{RESET}")
        print(f" {ROXO}[ 4  ]{RESET} {BRANCO}Verificar vulnerabilidade SQL (SQLMap) {ROXO}*Nova Aba*{RESET}")
        print(f" {ROXO}[ 5  ]{RESET} {BRANCO}Executar Ataque DDoS (GAMKERS-DDOS) {ROXO}*Nova Aba*{RESET}")
        print(f" {ROXO}[ 6  ]{RESET} {BRANCO}Módulo Wi-Fi (Aircrack-NG Suite) {ROXO}*Nova Aba*{RESET}")
        print(f" {ROXO}[ 7  ]{RESET} {BRANCO}Monitor de Rede (Tshark) {ROXO}*Nova Aba*{RESET}")
        print(f" {ROXO}[ 8  ]{RESET} {BRANCO}Módulo Quebra de Hashes (John) {ROXO}*Nova Aba*{RESET}")
        print(f" {ROXO}[ 9  ]{RESET} {BRANCO}Fern Wi-Fi Cracker (GUI) {ROXO}*Nova Aba*{RESET}")
        print(f" {ROXO}[ 10 ]{RESET} {BRANCO}Forçar Atualização / Reinstalação Geral{RESET}")
        print(f" {ROXO}[ 11 ]{RESET} {BRANCO}Sair{RESET}\n")

        opcao = input(f"{ROXO}Escolha uma operação -> {RESET}").strip()

        if opcao == "1":
            entrada = input(f"\n{BRANCO}Digite o Domínio ou IP: {RESET}").strip()
            if entrada:
                alvo = entrada.replace("https://", "").replace("http://", "").split("/")[0]
                log_mensagem("sucesso", f"Alvo definido para: {alvo}")
            time.sleep(1.2)

        elif opcao == "2":
            PortScanner(alvo).rodar()

        elif opcao == "3":
            WebFuzzer(alvo).rodar()

        elif opcao == "4":
            if not alvo:
                log_mensagem("erro", "Defina o alvo primeiro.")
                time.sleep(1)
                continue
            cmd = f"sqlmap -u http://{alvo} --batch --random-agent"
            abrir_em_nova_aba(cmd, titulo="SQLMap")

        elif opcao == "5":
            caminho_absoluto = os.path.abspath("GAMKERS-DDOS")
            cmd = f"cd {caminho_absoluto} && python3 GAMKERS-DDOS.py"
            abrir_em_nova_aba(cmd, titulo="DDoS Attack")

        elif opcao == "6":
            limpar_tela()
            exibir_logo()
            print(f"\n{BRANCO}--- MÓDULO WI-FI AIRCRACK ---{RESET}")
            interface = input(f"{BRANCO}Digite a interface modo monitor (ex: wlan0mon): {RESET}").strip()
            if interface:
                cmd = f"sudo airodump-ng {interface}"
                abrir_em_nova_aba(cmd, titulo="Airodump Scan")
            else:
                log_mensagem("erro", "Interface inválida.")
            input("\nEnter para continuar...")

        elif opcao == "7":
            interface = input(f"\n{BRANCO}Interface de Rede (Vazio para padrão): {RESET}").strip()
            cmd = f"sudo tshark -i {interface}" if interface else "sudo tshark"
            abrir_em_nova_aba(cmd, titulo="Packet Capture")

        elif opcao == "8":
            hash_file = input(f"\n{BRANCO}Arquivo de hashes: {RESET}").strip()
            if os.path.exists(hash_file):
                cmd = f"john {hash_file}"
                abrir_em_nova_aba(cmd, titulo="John The Ripper")
            else:
                log_mensagem("erro", "Arquivo não encontrado.")
                time.sleep(1.2)

        elif opcao == "9":
            caminho_fern = os.path.abspath("fern-wifi-cracker/Fern-Wifi-Cracker")
            cmd = f"cd {caminho_fern} && sudo python3 execute.py"
            abrir_em_nova_aba(cmd, titulo="Fern Wifi Cracker")

        elif opcao == "10":
            instalador.instalar_tudo()

        elif opcao == "11":
            log_mensagem("info", "Saindo do painel...")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{VERMELHO}[-] Encerrado pelo usuário.{RESET}")
        sys.exit(0)
