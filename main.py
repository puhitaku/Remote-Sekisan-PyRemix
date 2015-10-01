import socket, requests, json, codecs
from optparse import OptionParser
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config.update(
    PROPAGATE_EXCEPTIONS = True
)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/get_my_ip')
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.route('/acquire')
def acquire():
    client_ip = request.remote_addr
    #return 'wow', 200
    return acq_manager.acquire(client_ip)

@app.route('/free')
def free():
    client_ip = request.remote_addr
    return acq_manager.free(client_ip)

class AcquireManager:
    def __init__(self, user_dict):
        self.acquired_user = ''
        self.user_dict = user_dict
    def acquire(self, ip):
        if   self.acquired_user != '':
            res = ' '.join([self.acquired_user,'is using the service.'])
            return (res, 503)
        elif ip in self.user_dict:
            self.acquired_user = self.user_dict[ip]
            res = 'OK'
            return (res, 200)
        else:
            res = 'This IP address is not registered.'
            return (res, 404)

    def free(self, ip):
        if self.user_dict[ip] == self.acquired_user:
            self.acquired_user = ''
            res = {'OK'}
            return (res, 200)

def parse(usage):
    p = OptionParser(usage)

    p.add_option(
        '-m', '--mode',
        type='choice',
        choices=['client', 'server'],
        default='client',
        metavar='MODE',
        help='choose mode from "client" or "server"'
    )

    (opts, args) = p.parse_args()

    return opts, args

def main():
    print("""\
    Remote Sekisan Python-remix
    Takumi Sueda, 2014
    """)
    
    usage = 'usage: %prog [options] keyword'
    (options, args) = parse(usage)

    print('mode =', options.mode)

    if options.mode == 'server':
        f = codecs.open('setting_nakaken.json', 'r', 'utf-8')
        setting = json.loads(f.read())
        user = setting['user']

        acq_manager = AcquireManager(user)
        global acq_manager
        app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()