# -*- coding: UTF-8 -*-
import re
import requests


patt_item = '<div class="rightListsMain">(.*?)<div class="contentRight">'
patt_ip = r'\d+\.\d+\.\d+\.\d+'
patt_url = '<span class="aSpan"><a href="(.*?)"'
patt_title = '<p class="max-tow-row">\n +(.*)\n'
patt_port = r'<a class="portHover">(\d*?)</a>'
patt_protocol = r'class="whiteSpan protocolHover"><!---->\n +\b(.*?)\n'


patt_total = r'<span class="el-pagination__total">.? (\d*?) .?<'
patt_page = r'<li class="number">(\d*?)</li>'


domain = "fofa.info"


def ui_print_message(level, message):
    pass


def set_headers(header):
    global headers
    headers = header


def handle_content(page, content):
    url = ''
    ip = ''
    title = ''
    port = ''
    protocol = ''

    re_ip = re.search(patt_ip, content, flags=re.M)
    if re_ip:
        ip = re_ip.group(0)
    re_url = re.search(patt_url, content, flags=re.M)
    if re_url:
        url = re_url.group(1)
    re_title = re.search(patt_title, content, flags=re.M)
    if re_title:
        title = re_title.group(1)
    re_port = re.search(patt_port, content, flags=re.M)
    if re_port:
        port = re_port.group(1)
    re_protocol = re.search(patt_protocol, content, flags=re.M)
    if re_protocol:
        protocol = re_protocol.group(1)
    return [page, url, ip, title, port, protocol]


def crawling_content(qbase64, page: int, r: int) -> (list, str, int):
    params = {
        "qbase64": qbase64,
        "page": page
    }

    crawling_data = []

    try:
        res = requests.get("https://fofa.info/result", params=params, headers=headers, timeout=5, verify=False)
        re_list = re.findall(patt_item, res.text, flags=re.M | re.S)
        if len(re_list) == 0:
            return False, '', page, r

        for i in re_list:
            crawling_data.append(handle_content(page, i))
        return crawling_data, res.text, page, r
    except Exception as e:
        ui_print_message(2, "获取出错了！请检查 cookie 是否有效以及网络连接是否正常。")
        ui_print_message(2, e)
        return False, '', page, r


def crawling_info(qbase, cd_max_page):
    row_route = crawling_content(qbase, 1, 0)
    total = 0
    max_page = 0
    end_page = 0
    if row_route[0]:
        re_total = re.search(patt_total, row_route[1], flags=re.M)
        if re_total:
            total = re_total.group(1)
        re_page = re.findall(patt_page, row_route[1], re.M)
        if len(re_page):
            max_page = int(re_page[-1])
            end_page = min(cd_max_page, max_page)
    return total, max_page, end_page