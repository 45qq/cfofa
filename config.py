# -*- coding: UTF-8 -*-
import configparser
import os
from lib.utility import decode_base64, encode_base64


output_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "output")
data_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "config.ini")
config = configparser.ConfigParser()
if not os.path.exists(data_path):
    config.add_section('Proxy')
    config.set('Proxy', 'use_proxy', '0')
    config.set('Proxy', 'proxy_host', 'localhost')
    config.set('Proxy', 'proxy_port', '1080')
    config.add_section('User')
    config.set('User', 'fofa_cookie', '')
    config.set('User', 'start_page', '1')
    config.set('User', 'max_page', '10')
    config.set('User', 'output_mode', '0')
    config.set('User', 'qbase64', '')
    config.write(open(data_path, 'w', encoding='utf-8'))
else:
    config.read(data_path, 'utf-8')


class Cd:
    def __init__(self):
        self.use_proxy = config.getint('Proxy', 'use_proxy')
        self.proxy_host = config.get('Proxy', 'proxy_host')
        self.proxy_port = config.getint('Proxy', 'proxy_port')

        self.fofa_cookie = decode_base64(config.get('User', 'fofa_cookie'))
        self.start_page = config.getint('User', 'start_page')
        self.max_page = config.getint('User', 'max_page')
        self.output_mode = config.getint('User', 'output_mode')
        self.qbase64 = config.get('User', 'qbase64')
        self.q = decode_base64(self.qbase64)


cd = Cd()


def save_proxy(is_use_proxy, host, port):
    cd.use_proxy = is_use_proxy
    cd.proxy_host = host
    cd.proxy_port = port

    config.set('Proxy', 'use_proxy', str(cd.use_proxy))
    config.set('Proxy', 'proxy_host', cd.proxy_host)
    config.set('Proxy', 'proxy_port', str(cd.proxy_port))
    config.write(open(data_path, 'w', encoding='utf-8'))


def save_user(cookie, start_page, max_page, output_mode, q):
    cd.fofa_cookie = cookie
    cd.start_page = start_page
    cd.max_page = max_page
    cd.output_mode = output_mode
    cd.qbase64 = encode_base64(q)
    cd.q = q

    config.set('User', 'fofa_cookie', encode_base64(cookie))
    config.set('User', 'start_page', str(start_page))
    config.set('User', 'max_page', str(max_page))
    config.set('User', 'output_mode', str(output_mode))
    config.set('User', 'qbase64', cd.qbase64)
    config.write(open(data_path, 'w', encoding='utf-8'))


def save_output_mode(output_mode):
    cd.output_mode = output_mode
    config.set('User', 'output_mode', str(output_mode))
    config.write(open(data_path, 'w', encoding='utf-8'))
