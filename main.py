import socket, requests, json, codecs
from optparse import OptionParser
from flask import Flask, request, jsonify
from manager import AcquireManager, HeartBeatManager

app = Flask(__name__)
manager = AcquireManager()
heart = HeartBeatManager()

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/get_my_ip')
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.route('/acquire')
def acquire():
    client_ip = request.remote_addr
    if manager.acquire(client_ip):
        heart.born(callback=manager.free)
        return jsonify({'mes': 'OK'}), 200
    else:
        return jsonify({'mes': 'NG'}), 200

@app.route('/free')
def free():
    if manager.free():
        return jsonify({'mes': 'OK'}), 200
    else:
        return jsonify({'mes': 'NG'}), 200

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
        f = codecs.open('setting.json', 'r', 'utf-8')
        setting = json.loads(f.read())
        user = setting['user']
        manager.set_user_list(user)
        heart.set_ttl(setting['ttl'])

        app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()