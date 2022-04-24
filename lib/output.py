# -*- coding: UTF-8 -*-
import os
import time
import random
import csv
from lib.utility import get_output_head, get_head_index


output_dir: str


def new_output_dir(root):
    global output_dir
    if not os.path.exists(root):
        os.mkdir(root)
    output_dir = os.path.join(root, "%s_%d" % (time.strftime("%m-%d_%H-%M-%S", time.localtime()), random.randint(1000, 9999)))


def output_file(mode, q, data: list):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    data.sort(key=lambda item: item[0][0])

    if not os.path.exists(os.path.join(output_dir, "q.txt")):
        with open(os.path.join(output_dir, "q.txt"), 'w', encoding='utf-8') as f:
            f.write(q)

    if mode == 0:
        path = os.path.join(output_dir, "data.csv")
        if os.path.exists(path):
            return 0
        with open(path, 'w', newline='', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(get_output_head())
            for row in data:
                f_csv.writerows(row)
    elif mode == 1:
        path = os.path.join(output_dir, "data_url.txt")
        if os.path.exists(path):
            return 0
        url_list = []
        index = get_head_index("URL")
        with open(path, 'w', encoding='utf-8') as f:
            for group in data:
                for row in group:
                    if row[index] != '' and row[index] not in url_list:
                        f.write(row[index])
                        f.write('\n')
                        url_list.append(row[index])
    elif mode == 2:
        path = os.path.join(output_dir, "data_ip.txt")
        if os.path.exists(path):
            return 0
        ip_list = []
        index = get_head_index("IP")
        with open(path, 'w', encoding='utf-8') as f:
            for group in data:
                for row in group:
                    if row[index] not in ip_list:
                        f.write(row[index])
                        f.write('\n')
                        ip_list.append(row[index])

    return output_dir
