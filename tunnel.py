import os,time,threading,subprocess,requests,json

class TunnelManager:
    def __init__(self,port):
        self.port=port
        self.url=''

    def start(self,choice):
        if choice=='1':self._start_cloudflare()
        elif choice=='2':self._start_ngrok()
        elif choice=='3':self._start_serveo()
        elif choice=='4':self.url=f'localhost:{self.port}'

    def _start_cloudflare(self):
        def run():
            os.system(f'cloudflared tunnel --url http://localhost:{self.port} > logs/cf.log 2>&1')
        threading.Thread(target=run,daemon=True).start()
        time.sleep(5)
        try:
            with open('logs/cf.log')as f:
                for l in f:
                    if 'trycloudflare.com' in l:
                        self.url=l.strip().split()[-1]
                        break
        except:pass

    def _start_ngrok(self):
        def run():
            os.system(f'ngrok http {self.port} --log=stdout > logs/ngrok.log 2>&1')
        threading.Thread(target=run,daemon=True).start()
        time.sleep(3)
        try:
            r=requests.get('http://127.0.0.1:4040/api/tunnels',timeout=5)
            self.url=r.json()['tunnels'][0]['public_url']
        except:pass

    def _start_serveo(self):
        def run():
            os.system(f'ssh -o StrictHostKeyChecking=no -R 80:localhost:{self.port} serveo.net')
        threading.Thread(target=run,daemon=True).start()
        self.url='serveo.net'

    def show(self):
        if self.url:
            print(f'\033[1;32m[+] URL: {self.url}\033[0m')
        else:
            print(f'\033[1;33m[*] Tunnel starting...\033[0m')