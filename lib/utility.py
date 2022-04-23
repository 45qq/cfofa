# -*- coding: UTF-8 -*-
import browser_cookie3
import platform
import subprocess
import re
import base64
import requests
import socket
import socks
import os
from tkinter import StringVar

old_socksocket = None
output_head_list = ["#", "URL", "IP", "标题", "端口", "协议"]


def get_output_head():
    return output_head_list


def get_head_index(item):
    return output_head_list.index(item)


def ui_print_message(level, message):
    pass


def get_cookie_str(cj):
    cookie = ''
    cookie_dist = requests.utils.dict_from_cookiejar(cj)
    for name in cookie_dist:
        cookie += "%s=%s; " % (name, cookie_dist[name])
    return cookie


def get_cookie(domain):
    try:
        get_cookie_str(browser_cookie3.chrome(domain_name=domain))
        cookie = get_cookie_str(browser_cookie3.load(domain_name=domain))
        ui_print_message(2, "获得 Cookie：\n" + cookie)
        return cookie
    except Exception as e:
        if str(e).find("Chrome") >= 0 and platform.system() == "Windows":
            try:
                cmd = r'mklink "%LocalAppData%\Google\Chrome\User Data\Default\Cookies" "Network\Cookies"'
                subprocess.run(r'cmd /C "%s"' % cmd, shell=True)
                cookie = get_cookie_str(browser_cookie3.load(domain_name=domain))
                ui_print_message(2, "获得 Cookie：\n" + cookie)
                return cookie
            except Exception as e:
                ui_print_message(2, e)
    ui_print_message(2, "Cookie 自动获取失败！")
    return False


def check_int(var: StringVar) -> int:
    c = ''.join(re.findall('\d+', var.get()))
    if c == '':
        c = '1'
    var.set(c)
    return int(var.get())


def decode_base64(s):
    return str(base64.b64decode(s.encode('utf-8')), 'utf-8')


def encode_base64(s):
    return str(base64.b64encode(s.encode('utf-8')), 'utf-8')


def update_proxy(cd):
    global old_socksocket
    if cd.use_proxy:
        old_socksocket = socket.socket
        socks.set_default_proxy(socks.SOCKS5, cd.proxy_host, cd.proxy_port)
        socket.socket = socks.socksocket
        requests.session().keep_alive = False
    elif old_socksocket:
        socket.socket = old_socksocket


def open_fp(fp: str):
    system_type: str = platform.platform()
    if 'mac' in system_type:
        fp: str = fp.replace("\\", "/")
        subprocess.call(["open", fp])
    else:
        fp: str = fp.replace("/", "\\")
        os.startfile(os.path.join(fp, ''))
