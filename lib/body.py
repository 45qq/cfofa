# -*- coding: UTF-8 -*-
import threading
import urllib3
import lib.fofa as fofa
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
}

data = []
old_data = []
old_thead = None
thead_lock = threading.Lock()
thead_id = 0
total = 0
max_page = 0
end_page = 0
finished = True
wait_page = 0
count = 0
old_count = 0
page_count = 0
old_thead_id = 0
urllib3.disable_warnings()


def ui_print_message(level, message=''):
    pass


def ui_reset(tree):
    pass


def get_data():
    return data


def get_all_data():
    return old_data + data


def clear_old_data():
    old_data.clear()


def is_finished():
    return finished


def get_wait_page():
    return wait_page


def set_wait_page(tree, page):
    global wait_page, cd
    [tree.delete(item) for item in tree.get_children()]
    if not globals().get('cd'):
        return
    wait_page = min(max(page, cd.start_page), end_page)
    for i in data:
        if i[0][0] == wait_page:
            output_tree(tree, i)


def output_tree(tree, d):
    i = 1
    for row in d:
        tree.insert('', i, values=[i] + row[1:])
        i += 1
    ui_print_message(3, str(wait_page))


def theard_crawling_content(tid, qbase64, page: int, r: int):
    if tid != thead_id:
        ui_print_message(4)
        return
    return fofa.crawling_content(qbase64, page, r)


def start_search(tree, tid):
    if tid != thead_id:
        ui_print_message(4)
        return
    global old_thead, total, max_page, end_page, page_count, count
    if old_thead and old_thead.is_alive():
        old_thead.join()
    ui_reset(tree)
    if tid != thead_id:
        ui_print_message(4)
        return
    ui_print_message(0, "正在加载。。。")
    old_thead = threading.currentThread()

    [total, max_page, end_page] = fofa.crawling_info(cd.qbase64, cd.max_page)

    if tid != thead_id:
        ui_print_message(4)
        return

    if total == 0:
        ui_print_message(0, "查询为空！请检查 Cookie 是否有效和查询语句是否正确。")
        return
    elif total == -1:
        ui_print_message(0, "查询失败！请检查网络连接。")
        return

    ui_print_message(0, "共 %s 条，%d 页。" % (total, max_page))

    with ThreadPoolExecutor(max_workers=cd.cookie_thread_count) as t:
        obj_list = []
        for i in range(cd.start_page, end_page + 1):
            obj_list.append(t.submit(theard_crawling_content, tid, cd.qbase64, i, 0))

        count = 0
        page_count = 0
        fail_list = []
        flag = True
        while flag:
            if flag:
                flag = False
            if tid != thead_id:
                return

            for future in as_completed(obj_list):
                if tid != thead_id:
                    return
                row_route = future.result()

                if row_route[0]:
                    data.append(row_route[0])
                    if wait_page == row_route[2]:
                        output_tree(tree, row_route[0])

                    num = len(row_route[0])
                    count += num
                    page_count = page_count + 1
                    ui_print_message(1, "获取数据中……[当前 %d/%d 页 %d 条，总 %d 条]" % (page_count, max_page, num, count))
                elif row_route[3] < 10:
                    flag = True
                    fail_list.append(t.submit(fofa.crawling_content, cd.qbase64, row_route[2], row_route[3] + 1))
                else:
                    ui_print_message(2, "第 %d 页获取失败！" % row_route[2])
            wait(obj_list)
            obj_list = [i for i in fail_list]
            fail_list.clear()
            if flag:
                ui_print_message(2, "查询失败！2秒后尝试重新获取。")
                sleep(2)

        ui_print_message(1, "数据获取完成！获取 %d/%d 页，%d 条，旧查询 %d 条。" % (page_count, max_page, count, old_count))
        ui_print_message(2, "查询 %s 完成！" % cd.q)
        ui_print_message(4)


def process(tree):
    global finished
    finished = False
    thead = threading.Thread(target=start_search, args=(tree, thead_id))
    thead.start()
    thead.join()
    finished = True


def start(tree, c):
    global thead_id, cd, wait_page, old_data, old_count
    cd = c
    headers['cookie'] = cd.fofa_cookie
    fofa.set_headers(headers)
    wait_page = cd.start_page

    data.clear()

    thead_id = thead_id + 1
    threading.Thread(target=process, args=(tree,)).start()


def stop():
    global thead_id
    thead_id = thead_id + 1
    ui_print_message(1, "查询停止！获取 %d/%d 页，%d 条，旧查询 %d 条。" % (page_count, max_page, count, old_count))
    ui_print_message(2, "查询 %s 停止！" % cd.q)
    ui_print_message(4)


def save_to_old_date():
    global old_data, data, old_data, old_thead_id, old_count
    if old_thead_id == thead_id:
        ui_print_message(2, "已保留，不可重复保留！")
        return
    old_thead_id = thead_id
    old_data += data
    old_count = 0
    for i in old_data:
        old_count += len(i)
    ui_print_message(2, "已保留当前查询！保留 %d 条。" % old_count)
