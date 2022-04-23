# -*- coding: UTF-8 -*-
import threading
import urllib3
import lib.fofa as fofa
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
}

data = []
old_thead = None
thead_lock = threading.Lock()
thead_id = 0
total = 0
max_page = 0
end_page = 0
finished = True
wait_page = 0

urllib3.disable_warnings()


def ui_print_message(level, message):
    pass


def ui_reset(tree):
    pass


def get_data():
    return data


def is_finished():
    return finished


def get_wait_page():
    return wait_page


def set_wait_page(tree, page):
    global wait_page
    [tree.delete(item) for item in tree.get_children()]
    wait_page = min(max(page, cd.start_page), end_page)
    for i in data:
        if i[0][0] == wait_page:
            output_tree(tree, i)


def output_tree(tree, d):
    i = 1
    for row in d:
        tree.insert('', i, values=[i] + row[1:])
        i += 1
    ui_print_message(3, wait_page)


def start_search(tree, tid):
    global old_thead, total, max_page, end_page
    if old_thead and old_thead.is_alive():
        old_thead.join()
    ui_reset(tree)
    ui_print_message(0, "正在加载。。。")
    old_thead = threading.currentThread()

    [total, max_page, end_page] = fofa.crawling_info(cd.qbase64, cd.max_page)

    if total == 0:
        ui_print_message(0, "查询为空！请检查 Cookie 是否有效和查询语句是否正确。")
        return
    elif total == -1:
        ui_print_message(0, "查询失败！请检查网络连接。")
        return

    ui_print_message(0, "共 %s 条，%d 页。" % (total, max_page))

    with ThreadPoolExecutor(max_workers=20) as t:
        obj_list = []
        for i in range(cd.start_page, end_page + 1):
            obj_list.append(t.submit(fofa.crawling_content, cd.qbase64, i, 0))

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
                    ui_print_message(1, "正在获取数据中。。。[当前 %d 页 %d 条，总 %d 条]" % (page_count, num, count))
                elif row_route[3] < 5:
                    flag = True
                    fail_list.append(t.submit(fofa.crawling_content, cd.qbase64, row_route[2], row_route[3] + 1))
                else:
                    ui_print_message(1, "第 %d 页获取失败！" % row_route[2])
            wait(obj_list)
            obj_list = [i for i in fail_list]
            fail_list.clear()
        ui_print_message(1, "数据获取完成！获取 %d 页，%d 条。" % (page_count, count))
        ui_print_message(2, "查询 %s 完成！" % cd.q)
        ui_print_message(4, '')


def process(tree):
    global finished
    finished = False
    thead = threading.Thread(target=start_search, args=(tree, thead_id))
    thead.start()
    thead.join()
    finished = True


def start(tree, c):
    global thead_id, cd, wait_page
    cd = c
    headers['cookie'] = cd.fofa_cookie
    fofa.set_headers(headers)
    wait_page = cd.start_page
    data.clear()

    thead_id = thead_id + 1
    threading.Thread(target=process, args=(tree,)).start()
