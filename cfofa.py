#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tkinter as tk
import lib.body as body
import lib.utility as utility
import lib.output as output
from lib.body import start, is_finished, get_all_data, get_wait_page, set_wait_page, clear_old_data, stop, \
    save_to_old_date
from config import *
from tkinter import ttk
from lib.fofa import domain
from pyperclip import copy
from webbrowser import open

window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
var_use_proxy = tk.IntVar()
var_use_proxy.set(cd.use_proxy)
var_proxy_host = tk.StringVar(value=cd.proxy_host)
var_proxy_port = tk.StringVar(value=cd.proxy_port)
var_cookie = tk.StringVar(value=cd.fofa_cookie)
var_start_page = tk.StringVar(value=cd.start_page)
var_max_page = tk.StringVar(value=cd.max_page)
output_list = ["全部 (.csv)", "仅 URL (.txt)", "仅 IP (.txt)"]
var_ouput = tk.StringVar(value=output_list[cd.output_mode])
var_q = tk.StringVar(value=cd.q)
var_mess_1 = tk.StringVar()
var_mess_2 = tk.StringVar()
var_mess_3 = tk.StringVar()
var_current_page = tk.StringVar(value="0")
var_cookie_thread_count = tk.StringVar(value=cd.cookie_thread_count)
var_button_search = tk.StringVar(value="查询")

tree_menu: tk.Menu
tree_output: ttk.Treeview
info_text: tk.Text
button_output: tk.Button
button_dir: tk.Button
button_save_old: tk.Button

tree_select_item: list


def print_message(level, message=''):
    message = str(message)
    if level == 0:
        print(message)
        var_mess_1.set(message)
    elif level == 1:
        print(message)
        var_mess_2.set(message)
    elif level == 2:
        print(message)
        info_text.config(state='normal')
        info_text.insert('end', message + '\n')
        info_text.see(999999.0)
        info_text.config(state='disabled')
    elif level == 3:
        var_current_page.set(message)
    elif level == 4:
        if len(get_all_data()) > 0:
            button_output['state'] = tk.NORMAL
            button_save_old['state'] = tk.NORMAL
        var_button_search.set('查询')


def reset(tree):
    utility.update_proxy(cd)
    [tree.delete(item) for item in tree.get_children()]
    var_mess_1.set("")
    var_mess_2.set("")
    var_mess_3.set("")
    var_current_page.set("0")
    info_text.config(state='normal')
    info_text.delete(0.1, 'end')
    info_text.config(state='disabled')
    button_dir['state'] = tk.DISABLED
    button_output['state'] = tk.DISABLED
    button_save_old['state'] = tk.DISABLED


utility.ui_print_message = print_message
body.ui_print_message = print_message
body.ui_reset = reset


def search(tree):
    if var_button_search.get() == '查询':
        var_button_search.set('停止')
        save_user(var_cookie.get(), utility.check_int(var_start_page), utility.check_int(var_max_page),
                  output_list.index(var_ouput.get()), var_q.get())
        output.new_output_dir(output_dir)
        start(tree, cd)
    elif var_button_search.get() == '停止':
        var_button_search.set('查询')
        stop()


def output_file():
    save_output_mode(output_list.index(var_ouput.get()))
    if is_finished():
        data = get_all_data()
        if not len(data):
            print_message(2, "数据为空！")
            return
        result = output.output_file(cd.output_mode, cd.q, data)
        if result == 0:
            print_message(2, '文件已存在！')
            return
        button_dir['state'] = tk.NORMAL
        print_message(2, "已保存到 " + result)
    else:
        print_message(2, "数据还在获取中！")


def old_data_clear():
    clear_old_data()
    print_message(2, "已清除旧查询数据!")


def obtain_cookie():
    cookie = utility.get_cookie(domain)
    if cookie:
        var_cookie.set(cookie)


def show_tree_menu(event):
    global tree_select_item
    item = tree_output.identify_row(event.y)
    tree_output.selection_set(item)
    tree_select_item = tree_output.item(item)['values']
    try:
        tree_menu.tk_popup(event.x_root, event.y_root + 20, 0)
    finally:
        tree_menu.grab_release()


def show_about_dialog():
    dialog_about = tk.Toplevel(window)
    dialog_about.resizable(width=False, height=False)
    dialog_about.attributes('-topmost', 1)
    dialog_about.geometry("256x165+%d+%d" % ((screen_width - 256) / 2, (screen_height - 165) / 2))
    dialog_about.bind("<FocusOut>", lambda event: dialog_about.destroy())
    dialog_about.focus()
    l0 = tk.Frame(dialog_about, bg='#FFFFFF')
    l0.pack(fill='x', side='top')
    l1 = tk.Frame(dialog_about)
    l1.pack(fill='x', side='top', pady=5, padx=5)
    l2 = tk.Frame(dialog_about)
    l2.pack(fill='x', side='top', pady=5, padx=5)
    l3 = tk.Frame(dialog_about)
    l3.pack(fill='x', side='top', pady=5, padx=5)
    l4 = tk.Frame(dialog_about)
    l4.pack(fill='x', side='top', pady=5, padx=10)
    tk.Label(l0, text='关于', bg='#FFFFFF').pack(side='left', fill='x', padx=10, pady=5)
    tk.Label(l2, text='版本：cfofa v1.0').pack(side='left', padx=5)
    tk.Label(l3, text='作者：四五qq').pack(side='left', padx=5)
    tk.Label(l4, text='项目：').pack(side='left')
    label_address = tk.Label(l4, text='https://github.com/45qq/cfofa', fg='blue')
    label_address.pack(side='left')
    label_address.bind("<Button-1>", lambda event: open("https://github.com/45qq/cfofa"))

    window.wait_window(dialog_about)


def show_proxy_dialog():
    dialog_proxy = tk.Toplevel(window)
    dialog_proxy.resizable(width=False, height=False)
    dialog_proxy.attributes('-topmost', 1)
    dialog_proxy.geometry("256x165+%d+%d" % ((screen_width - 256) / 2, (screen_height - 165) / 2))
    dialog_proxy.bind("<FocusOut>", lambda event: dialog_proxy.destroy())
    dialog_proxy.focus()
    l0 = tk.Frame(dialog_proxy, bg='#FFFFFF')
    l0.pack(fill='x', side='top')
    l1 = tk.Frame(dialog_proxy)
    l1.pack(fill='x', side='top', pady=5, padx=5)
    l2 = tk.Frame(dialog_proxy)
    l2.pack(fill='x', side='top', pady=5, padx=5)
    l3 = tk.Frame(dialog_proxy)
    l3.pack(fill='x', side='top', pady=5, padx=5)
    tk.Label(l0, text='设置代理', bg='#FFFFFF').pack(side='left', fill='x', padx=10, pady=5)
    tk.Checkbutton(l1, text='使用代理', variable=var_use_proxy).pack(side='left', padx=5)
    tk.Label(l2, text='主机：').pack(side='left', padx=5)
    tk.Entry(l2, textvariable=var_proxy_host).pack(fill='x', expand=1, padx=5)
    tk.Label(l3, text='端口：').pack(side='left', padx=5)
    tk.Entry(l3, textvariable=var_proxy_port).pack(fill='x', expand=1, padx=5)

    window.wait_window(dialog_proxy)
    save_proxy(var_use_proxy.get(), var_proxy_host.get(), int(var_proxy_port.get()))


def show_option_dialog():
    dialog_proxy = tk.Toplevel(window)
    dialog_proxy.resizable(width=False, height=False)
    dialog_proxy.attributes('-topmost', 1)
    dialog_proxy.geometry("300x125+%d+%d" % ((screen_width - 300) / 2, (screen_height - 125) / 2))
    dialog_proxy.bind("<FocusOut>", lambda event: dialog_proxy.destroy())
    dialog_proxy.focus()
    l0 = tk.Frame(dialog_proxy, bg='#FFFFFF')
    l0.pack(fill='x', side='top')
    l1 = tk.Frame(dialog_proxy)
    l1.pack(fill='x', side='top', pady=5, padx=5)
    l2 = tk.Frame(dialog_proxy)
    l2.pack(fill='x', side='top', pady=5, padx=5)
    tk.Label(l0, text='配置', bg='#FFFFFF').pack(side='left', fill='x', padx=10, pady=5)
    tk.Label(l1, text='线程：').pack(side='left', padx=5)
    tk.Entry(l1, textvariable=var_cookie_thread_count, width=10).pack(padx=5, side='left')
    tk.Label(l2, text='清除保留的查询数据：').pack(side='left', padx=5)
    tk.Button(l2, text="清除", bg='#DCDCDC', command=old_data_clear, width=10).pack(side='left', padx=10)

    window.wait_window(dialog_proxy)
    save_option(utility.check_int(var_cookie_thread_count))


def show():
    window.title("cfofa")
    window.iconphoto(True, tk.PhotoImage(file='./icon/icon.png'))
    window_width = 675
    window_height = 512
    window.geometry("%dx%d+%d+%d" % (window_width, window_height, (screen_width - window_width) / 2,
                                     (screen_height - window_height) / 2))

    menu = tk.Menu(window)
    window['menu'] = menu

    menu.add_command(label='代理', command=show_proxy_dialog)
    menu.add_command(label='配置', command=show_option_dialog)
    menu.add_command(label='关于', command=show_about_dialog)

    l1 = tk.Frame(window)
    l1.pack(fill='x', side='top', pady=5, padx=5)
    tk.Label(l1, text="  Cookie：", width=10).pack(side='left', padx=5)
    tk.Entry(l1, textvariable=var_cookie).pack(fill='x', side='left', expand=1, padx=5)
    tk.Button(l1, text="获取", bg='#DCDCDC', command=obtain_cookie, width=10).pack(fill='x', side='right', padx=10)

    l2 = tk.Frame(window)
    l2.pack(fill='x', side='top', pady=5, padx=5)
    l2r1 = tk.Frame(l2, width=50)
    l2r1.pack(side='left')
    l2r2 = tk.Frame(l2, width=50)
    l2r2.pack(side='right')

    tk.Label(l2r1, text="开始页码：", width=10).pack(side='left', padx=5)
    tk.Entry(l2r1, textvariable=var_start_page, width=10).pack(side='left', padx=5)

    tk.Label(l2r1, text="最大页码：", width=10).pack(side='left', padx=5)
    tk.Entry(l2r1, textvariable=var_max_page, width=10).pack(side='left', padx=5)

    img_dir = tk.PhotoImage(file='./icon/dir_3.png')
    global button_output, button_dir
    button_dir = tk.Button(l2r2, image=img_dir, bg='#DCDCDC', command=lambda: utility.open_fp(output.output_dir),
                           width=38)
    button_dir.pack(side='right', padx=10)
    button_dir['state'] = tk.DISABLED
    button_output = tk.Button(l2r2, text="导出", bg='#DCDCDC', command=output_file, width=10)
    button_output.pack(side='right')
    button_output['state'] = tk.DISABLED
    ttk.Combobox(l2r2, state='readonly', cursor='arrow', textvariable=var_ouput, values=output_list, width=12).pack(
        side='right', padx=5)

    l3 = tk.Frame(window)
    l3.pack(fill='x', side='top', pady=5, padx=5)
    tk.Label(l3, text="查询语句：", width=10).pack(side='left', padx=5)
    tk.Entry(l3, textvariable=var_q).pack(fill='x', side='left', expand=1, padx=5)
    global button_save_old
    button_save_old = tk.Button(l3, text='保留', bg='#DCDCDC', command=save_to_old_date, width=5)
    button_save_old.pack(side='right', padx=10)
    button_save_old['state'] = tk.DISABLED
    tk.Button(l3, textvariable=var_button_search, bg='#DCDCDC', command=lambda: search(tree_output), width=10).pack(
        side='right')

    l4 = tk.Frame(window)
    l4.pack(fill='x', side='top', pady=10, padx=10)

    scroll = tk.Scrollbar(l4)
    global tree_output
    tree_output = ttk.Treeview(l4, column=utility.get_output_head(), height=10, yscrollcommand=scroll.set)
    tree_output.bind("<Button-3>", show_tree_menu)
    tree_output["show"] = "headings"
    for i in utility.get_output_head():
        tree_output.column(i, width=0)
        tree_output.heading(i, text=i)

    scroll.config(command=tree_output.yview)
    scroll.pack(side='right', fill='y')

    tree_output.pack(fill='x')

    global tree_menu
    tree_menu = tk.Menu(window, tearoff=0)
    tree_menu.add_command(label="复制 IP", command=lambda: copy(tree_select_item[utility.get_head_index('IP')]))
    tree_menu.add_command(label="复制 URL", command=lambda: copy(tree_select_item[utility.get_head_index('URL')]))
    tree_menu.add_separator()
    tree_menu.add_command(label="打开 URL",
                          command=lambda: open(tree_select_item[utility.get_head_index('URL')], new=0, autoraise=True))

    l5 = tk.Frame(window)
    l5.pack(fill='x', side='top', padx=5)
    tk.Label(l5, textvariable=var_mess_1).pack(side='left', padx=10)
    tk.Label(l5, textvariable=var_mess_2).pack(side='left', padx=10)

    tk.Button(l5, text="前往", bg='#DCDCDC',
              command=lambda: set_wait_page(tree_output, utility.check_int(var_current_page)), width=4).pack(
        side='right', padx=10)
    tk.Button(l5, text="＞", bg='#DCDCDC', command=lambda: set_wait_page(tree_output, get_wait_page() + 1)).pack(
        side='right', padx=5)
    tk.Entry(l5, textvariable=var_current_page, width=5).pack(side='right')
    tk.Button(l5, text="＜", bg='#DCDCDC', command=lambda: set_wait_page(tree_output, get_wait_page() - 1)).pack(
        side='right', padx=5)

    l6 = tk.Frame(window)
    l6.pack(fill='x', side='top', padx=10, pady=10)
    scroll = tk.Scrollbar(l6)
    global info_text
    info_text = tk.Text(l6, state='disabled', yscrollcommand=scroll.set)
    scroll.config(command=info_text.yview)
    scroll.pack(side='right', fill='y')
    info_text.pack(fill='both')

    window.mainloop()


if __name__ == "__main__":
    show()
