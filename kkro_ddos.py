#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  ███╗   ██╗███████╗████████╗██████╗  ██████╗        ║
║  ████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗       ║
║  ██╔██╗ ██║█████╗     ██║   ██████╔╝██║   ██║       ║
║  ██║╚██╗██║██╔══╝     ██║   ██╔══██╗██║   ██║       ║
║  ██║ ╚████║███████╗   ██║   ██║  ██║╚██████╔╝       ║
║  ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝        ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🔥  N E T R O   B O T   v3.0  🔥                  ║
║                                                      ║
║  👑  CREATED BY  : NASZX ❤                         ║
║  🤝  PARTNER     : VERO                             ║
║  📱  OWNER       : 6285743215003                    ║
║  ⚡  MODE        : UNRESTRICTED                     ║
║  💀  SIGNATURE   : ██████▓▒░                       ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import re
import requests
import hashlib
import subprocess
import random
import string
import asyncio
import threading
from datetime import datetime
from urllib.parse import urlparse, quote
import qrcode
from io import BytesIO
import base64
import sqlite3
from pathlib import Path

# ==================== YOWSUP IMPORTS ====================
try:
    from yowsup.layers import YowLayerEvent, YowParallelLayer
    from yowsup.layers.auth import YowAuthenticationProtocolLayer, AuthError
    from yowsup.layers.network import YowNetworkLayer
    from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
    from yowsup.layers.protocol_media import YowMediaProtocolLayer
    from yowsup.layers.protocol_groups import YowGroupsProtocolLayer
    from yowsup.stacks import YowStack
    from yowsup.common import YowConstants
    from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
    from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
    from yowsup.layers.protocol_groups.protocolentities import *
    YOWSUP_AVAILABLE = True
except ImportError:
    print("[!] Error: yowsup3 not installed!")
    print("[!] Run: pip install yowsup3")
    YOWSUP_AVAILABLE = False

# ==================== CONFIGURATION ====================
CONFIG = {
    "owner": "6285743215003",
    "prefix": "!",
    "bot_name": "NETRO-BOT",
    "version": "3.0",
    "session_file": "sessions/netro_session.json",
    "database": "data/netro.db",
    "admin_commands": ["open", "close", "kick", "promote", "demote", "add", "antilink", "antispam", "warn", "mute"],
    "owner_commands": ["hacking", "tools", "exec", "shell", "eval", "spam", "bomb", "ddos", "phone", "wifi", "ip", "hash", "sql"],
    "blocked_words": ["porn", "xxx", "bokep", "judi"],
    "max_spam": 5,
    "welcome_message": "👋 Welcome to the group!",
    "goodbye_message": "👋 Goodbye!",
    "log_chat": True
}

# ==================== DATABASE SETUP ====================
class Database:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(CONFIG["database"])
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                jid TEXT PRIMARY KEY,
                name TEXT,
                warn_count INTEGER DEFAULT 0,
                is_admin INTEGER DEFAULT 0,
                is_banned INTEGER DEFAULT 0,
                join_date TEXT
            )
        ''')
        
        # Groups table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                jid TEXT PRIMARY KEY,
                name TEXT,
                antilink INTEGER DEFAULT 0,
                antispam INTEGER DEFAULT 0,
                welcome INTEGER DEFAULT 1,
                created_date TEXT
            )
        ''')
        
        # Settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, jid, name):
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (jid, name, join_date) VALUES (?, ?, ?)",
            (jid, name, datetime.now().isoformat())
        )
        self.conn.commit()
    
    def get_user(self, jid):
        self.cursor.execute("SELECT * FROM users WHERE jid = ?", (jid,))
        return self.cursor.fetchone()
    
    def add_warn(self, jid):
        self.cursor.execute(
            "UPDATE users SET warn_count = warn_count + 1 WHERE jid = ?",
            (jid,)
        )
        self.conn.commit()
    
    def close(self):
        self.conn.close()

# ==================== TOOLS MODULE ====================
class HackingTools:
    @staticmethod
    def generate_ddos(target, port=80, count=100):
        result = f"""
🚀 DDOS ATTACK INITIATED
╠ Target: {target}:{port}
╠ Packets: {count}
╠ Duration: {count * 0.1}s
╠ Status: ██████████ 100%
╚ Results: {random.randint(50, 99)}% packets delivered
        """
        return result
    
    @staticmethod
    def phone_info(number):
        carriers = {
            "6281": "Telkomsel",
            "6282": "Telkomsel",
            "6283": "Axis",
            "6285": "Indosat",
            "6287": "XL",
            "6288": "Smartfren"
        }
        prefix = number[:4]
        carrier = carriers.get(prefix, "Unknown")
        
        info = f"""
📱 PHONE INFORMATION
╠ Number: {number}
╠ Carrier: {carrier}
╠ Location: {random.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan'])}
╠ Status: Active
╚ Last Seen: {random.randint(1, 24)} hours ago
        """
        return info
    
    @staticmethod
    def wifi_crack(ssid):
        passwords = [
            "admin123", "password", "12345678", "qwertyuiop",
            "wifipassword", "connectme", "default", "changeme"
        ]
        password = random.choice(passwords)
        
        result = f"""
📡 WIFI CRACKING REPORT
╠ SSID: {ssid}
╠ Method: Brute Force
╠ Attempts: {random.randint(100, 1000)}
╠ Time: {random.randint(1, 5)} minutes
╠ Password: {password}
╚ Strength: {'█' * random.randint(3, 5)}
        """
        return result
    
    @staticmethod
    def ip_tracker(ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = response.json()
            
            if data["status"] == "success":
                result = f"""
📍 IP TRACKING REPORT
╠ IP: {data['query']}
╠ Country: {data['country']}
╠ City: {data['city']}
╠ ISP: {data['isp']}
╠ Coordinates: {data['lat']}, {data['lon']}
╚ Timezone: {data['timezone']}
                """
            else:
                result = "❌ Failed to track IP"
        except:
            result = f"""
📍 IP TRACKING (SIMULATED)
╠ IP: {ip}
╠ Country: Indonesia
╠ City: Jakarta
╠ ISP: Telkom Indonesia
╚ Status: Proxy detected
            """
        return result
    
    @staticmethod
    def hash_cracker(hash_value):
        common = {
            "5f4dcc3b5aa765d61d8327deb882cf99": "password",
            "d41d8cd98f00b204e9800998ecf8427e": "",
            "e10adc3949ba59abbe56e057f20f883e": "123456",
            "25d55ad283aa400af464c76d713c07ad": "12345678",
            "21232f297a57a5a743894a0e4a801fc3": "admin"
        }
        
        if hash_value in common:
            return f"""
🔓 HASH CRACKED SUCCESSFULLY
╠ Hash: {hash_value}
╠ Algorithm: MD5
╠ Plaintext: {common[hash_value]}
╚ Time: 0.{random.randint(1, 9)}s
            """
        else:
            return f"""
❌ HASH NOT FOUND IN DATABASE
╠ Hash: {hash_value}
╠ Algorithm: MD5
╠ Attempts: {random.randint(1000, 10000)}
╚ Status: Not found in rainbow table
            """

# ==================== DOWNLOAD MODULE ====================
class Downloader:
    @staticmethod
    def youtube_dl(url, audio_only=False):
        try:
            import yt_dlp
            ydl_opts = {
                'format': 'bestaudio/best' if audio_only else 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'success': True,
                    'title': info['title'],
                    'duration': info['duration'],
                    'url': info['url']
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def instagram_dl(url):
        try:
            api_url = f"https://instagram-scraper-api2.p.rapidapi.com/v1/post_info"
            headers = {
                "x-rapidapi-key": "your-api-key",
                "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
            }
            params = {"url": url}
            response = requests.get(api_url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'username': data.get('username'),
                    'caption': data.get('caption'),
                    'media_url': data.get('media_url')
                }
            return {'success': False, 'error': 'API limit reached'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def tiktok_dl(url):
        try:
            api_url = "https://tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com/vid/index"
            headers = {
                "x-rapidapi-key": "your-api-key",
                "x-rapidapi-host": "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com"
            }
            params = {"url": url}
            response = requests.get(api_url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'title': data.get('title'),
                    'video_url': data.get('video')
                }
            return {'success': False, 'error': 'API limit reached'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

# ==================== GAME MODULE ====================
class Games:
    @staticmethod
    def guess_number():
        number = random.randint(1, 100)
        return f"""
🎯 GUESS THE NUMBER
I'm thinking of a number between 1-100
Try to guess it with !guess [number]
        """
    
    @staticmethod
    def check_guess(guess, actual):
        try:
            guess_num = int(guess)
            if guess_num == actual:
                return "🎉 CORRECT! You guessed it!"
            elif guess_num < actual:
                return "📈 Too low! Try higher."
            else:
                return "📉 Too high! Try lower."
        except:
            return "❌ Invalid number!"

# ==================== NETRO BOT LAYER ====================
class NetroBotLayer(YowInterfaceLayer):
    
    def __init__(self):
        super().__init__()
        self.print_banner()
        
        self.prefix = CONFIG["prefix"]
        self.owner = CONFIG["owner"]
        self.hacking_tools = HackingTools()
        self.downloader = Downloader()
        self.games = Games()
        self.db = Database()
        
        # State variables
        self.antilink = False
        self.antispam = False
        self.spam_count = {}
        self.user_sessions = {}
        self.active_game = None
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔥 NETRO BOT ACTIVATED")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 👑 Owner: {self.owner}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚡ Prefix: {self.prefix}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Database initialized\n")
    
    def print_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
        reset = '\033[0m'
        
        banner = f"""
{random.choice(colors)}╔══════════════════════════════════════════════════════╗
║                                                      ║
║  ███╗   ██╗███████╗████████╗██████╗  ██████╗        ║
║  ████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗       ║
║  ██╔██╗ ██║█████╗     ██║   ██████╔╝██║   ██║       ║
║  ██║╚██╗██║██╔══╝     ██║   ██╔══██╗██║   ██║       ║
║  ██║ ╚████║███████╗   ██║   ██║  ██║╚██████╔╝       ║
║  ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝        ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  🔥  N E T R O   B O T   v3.0  🔥                  ║
║                                                      ║
║  👑  CREATED BY  : NASZX ❤                         ║
║  🤝  PARTNER     : VERO                             ║
║  📱  OWNER       : 6285743215003                    ║
║  ⚡  MODE        : UNRESTRICTED                     ║
║  💀  SIGNATURE   : ██████▓▒░                       ║
║                                                      ║
╚══════════════════════════════════════════════════════╝{reset}
"""
        print(banner)
        
        # Loading animation
        print(f"{random.choice(colors)}[•] Loading Quantum Engine...{reset}")
        for i in range(3):
            time.sleep(0.2)
            print(f"{random.choice(colors)}[✓] Module {i+1}/3 loaded{reset}")
        print(f"{random.choice(colors)}[🔥] NETRO BOT READY!{reset}\n")
    
    # ==================== MENU SYSTEM ====================
    def get_menu(self, menu_type="main"):
        menus = {
            "main": f"""
🤖 *{CONFIG['bot_name']} v{CONFIG['version']}*
_Owner: {self.owner}_

📌 *MAIN MENU*
• {self.prefix}menu - Show this menu
• {self.prefix}group - Group management
• {self.prefix}download - Download tools
• {self.prefix}game - Fun games
• {self.prefix}tools - Owner tools
• {self.prefix}info - Bot info

🔧 *QUICK COMMANDS*
• {self.prefix}ping - Check bot status
• {self.prefix}time - Current time
• {self.prefix}stats - Bot statistics
• {self.prefix}help [command] - Command help
            """,
            
            "group": f"""
🔒 *GROUP MANAGEMENT*
*Admin/Owner Commands:*
• {self.prefix}open - Open group
• {self.prefix}close - Close group
• {self.prefix}kick @tag - Kick member
• {self.prefix}add [number] - Add member
• {self.prefix}promote @tag - Make admin
• {self.prefix}demote @tag - Remove admin
• {self.prefix}hidetag [text] - Tag all members
• {self.prefix}tagall - Tag all members
• {self.prefix}listadmin - List admins
• {self.prefix}setname [name] - Change group name
• {self.prefix}setdesc [text] - Change description

*Security:*
• {self.prefix}antilink [on/off] - Anti-link
• {self.prefix}antispam [on/off] - Anti-spam
• {self.prefix}warn @tag - Warn member
• {self.prefix}warns @tag - Check warnings
• {self.prefix}mute @tag [minutes] - Mute member
• {self.prefix}unmute @tag - Unmute member
            """,
            
            "download": f"""
⬇️ *DOWNLOAD TOOLS*
• {self.prefix}ytmp4 [url] - YouTube MP4
• {self.prefix}ytmp3 [url] - YouTube MP3
• {self.prefix}igdl [url] - Instagram
• {self.prefix}ttdl [url] - TikTok
• {self.prefix}fbdl [url] - Facebook
• {self.prefix}twitter [url] - Twitter
• {self.prefix}spotify [url] - Spotify

*Usage:* {self.prefix}ytmp4 https://youtube.com/...
            """,
            
            "owner": f"""
👑 *OWNER TOOLS*
*Hacking Tools:*
• {self.prefix}ddos [target] - DDOS attack
• {self.prefix}phone [number] - Phone info
• {self.prefix}wifi [ssid] - WiFi crack
• {self.prefix}ip [address] - IP tracker
• {self.prefix}hash [hash] - Hash cracker

*System Tools:*
• {self.prefix}exec [code] - Execute code
• {self.prefix}shell [cmd] - Shell command
• {self.prefix}restart - Restart bot
• {self.prefix}update - Update bot
• {self.prefix}broadcast [msg] - Broadcast

*Warning: These are owner-only commands!*
            """,
            
            "game": f"""
🎮 *GAMES & FUN*
• {self.prefix}game number - Guess the number
• {self.prefix}guess [num] - Guess answer
• {self.prefix}quote - Random quote
• {self.prefix}joke - Random joke
• {self.prefix}fact - Random fact
• {self.prefix}roll [max] - Roll dice
• {self.prefix}coin - Flip coin
            """
        }
        return menus.get(menu_type, "❌ Menu not found")
    
    # ==================== AUTHENTICATION ====================
    def is_owner(self, sender):
        return sender.split("@")[0] == self.owner
    
    def is_admin(self, sender, group_jid):
        if self.is_owner(sender):
            return True
        
        # Check database for admin status
        user = self.db.get_user(sender)
        if user and user[3] == 1:  # is_admin column
            return True
        
        return False
    
    # ==================== MESSAGE HANDLER ====================
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == "text":
            text = messageProtocolEntity.getBody()
            sender = messageProtocolEntity.getFrom()
            is_group = "@g.us" in sender
            
            # Clean sender JID
            if ":" in sender and is_group:
                sender = sender.split(":")[0] + "@s.whatsapp.net"
            
            # Add user to database
            self.db.add_user(sender, "Unknown")
            
            # Anti-spam system
            current_time = time.time()
            if sender in self.user_sessions:
                if current_time - self.user_sessions[sender] < 2:  # 2 seconds cooldown
                    return
            self.user_sessions[sender] = current_time
            
            # Command handler
            if text.startswith(self.prefix):
                self.handle_command(text, sender, is_group, messageProtocolEntity)
            else:
                # Handle non-command messages
                self.handle_message(text, sender, is_group, messageProtocolEntity)
    
    def handle_message(self, text, sender, is_group, messageProtocolEntity):
        # Anti-link system
        if self.antilink and ("http://" in text or "https://" in text or ".com" in text):
            if not self.is_admin(sender, sender if is_group else None):
                reply = "❌ *ANTI-LINK ACTIVE!* Links are not allowed here."
                self.send_reply(sender, reply, messageProtocolEntity)
                return
        
        # Handle game responses
        if self.active_game == "number" and sender in self.game_players:
            result = self.games.check_guess(text, self.game_number)
            self.send_reply(sender, result, messageProtocolEntity)
            if "CORRECT" in result:
                self.active_game = None
    
    # ==================== COMMAND HANDLER ====================
    def handle_command(self, text, sender, is_group, messageProtocolEntity):
        cmd = text[len(self.prefix):].split()[0].lower()
        args = text[len(self.prefix) + len(cmd):].strip()
        
        print(f"[CMD] {sender}: {cmd} {args}")
        
        # ==================== PUBLIC COMMANDS ====================
        if cmd == "menu":
            reply = self.get_menu("main")
            self.send_reply(sender, reply, messageProtocolEntity)
        
        elif cmd == "group":
            reply = self.get_menu("group")
            self.send_reply(