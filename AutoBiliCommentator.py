# 导入 Tkinter 库
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

# 导入 Selenium 相关模块
from selenium import webdriver
from selenium.webdriver.common.by import By  # 提供不同的定位策略
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 导入请求库
import requests

# 导入用于 URL 编码的模块
from urllib.parse import quote

# 导入生成随机字符串的模块
import random
import string

# 其他模块
import time
import sys

class GUI:
    # 类变量
    CITY_NAME = ""
    COMMENT_CONTENT = ""
    COOKIE = ""
    DP_COOKIE = ""
    NUMBER = ""
    TIME = ""

    # 运行
    def run(self):
        # 运行主循环
        self.root.mainloop()

    # 初始化
    def __init__(self):
        # 输入框(城市)，默认为空
        self.city_entry = None
        # 创建主窗口
        self.root = tk.Tk()
        # 调用setup_main_window方法
        self.setup_main_window()
        # 捕捉窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    # 设置窗口
    def setup_main_window(self):
        # 设置主题
        style = ttk.Style()
        # style.theme_use('winnative')
        style.theme_use('clam')

        # 设置窗口大小
        # self.root.geometry("500x400")
        self.root.geometry("680x350")

        # 设置标题
        self.root.title("Bilibili会员购 - 自动评论工具 v1.0")

        # 第一行
        # 设置标签(城市)
        label_city = tk.Label(self.root, text="城市：", font=("KaiTi", 18))
        label_city.grid(row=0, column=0, padx=10, pady=10)
        # 创建输入框
        self.city_entry = ttk.Entry(self.root, font=("KaiTi", 18))
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)
        # 默认：成都
        self.city_entry.insert(0, "成都")
        # 设置按钮(选择城市)
        city_button = ttk.Button(self.root, text="选择城市", command=self.show_cities, style="TButton")
        city_button.grid(row=0, column=2, padx=10, pady=0)

        # 第二行
        # 设置标签(评论内容)
        label_comment = tk.Label(self.root, text="评论内容：", font=("KaiTi", 18))
        label_comment.grid(row=1, column=0, padx=5)
        # 创建输入框
        self.comment_entry = ttk.Entry(self.root, font=("KaiTi", 18))
        self.comment_entry.grid(row=1, column=1, padx=10)

        # 第三行
        # 设置标签(Cookie)
        label_cookie = tk.Label(self.root, text="COOKIE：", font=("KaiTi", 18))
        label_cookie.grid(row=2, column=0, padx=10, pady=10)
        # 创建输入框
        self.cookie_entry = ttk.Entry(self.root, font=("KaiTi", 18))
        self.cookie_entry.grid(row=2, column=1, padx=10, pady=10)

        '''
        # 第四行
        # 设置标签(详情页Cookie)
        label_type = tk.Label(self.root, text="Cookie2：")
        label_type.grid(row=3, column=0, padx=5)
        # 创建输入框
        self.dp_cookie_entry = ttk.Entry(self.root)
        self.dp_cookie_entry.grid(row=3, column=1, padx=5)
        '''

        # 第四行
        label_number = tk.Label(self.root, text="评论数量(单页)：", font=("KaiTi", 18))
        label_number.grid(row=3, column=0, padx=10, pady=10)
        # 创建输入框
        self.number_entry = ttk.Entry(self.root, font=("KaiTi", 18))
        self.number_entry.grid(row=3, column=1, padx=10, pady=10)

        # 第五行
        label_time = tk.Label(self.root, text="评论间隔时间(单位:分)：", font=("KaiTi", 18))
        label_time.grid(row=4, column=0, padx=10, pady=10)
        # 创建输入框
        self.time_entry = ttk.Entry(self.root, font=("KaiTi", 18))
        self.time_entry.grid(row=4, column=1, padx=10, pady=10)

        # 第六行
        # 设置按钮(开始评论)
        comment_button = ttk.Button(self.root, text="开始评论", command=self.start_comment)
        comment_button.grid(row=5, column=0, padx=10, pady=10)

    def show_cities(self):
        # 创建子窗口
        city_window = tk.Toplevel(self.root)
        city_window.title("选择城市")

        # 创建列表框
        city_listbox = tk.Listbox(city_window, selectmode=tk.SINGLE)
        city_listbox.pack(side="left", pady=20)

        # 定义城市列表
        cities = ["全国", "上海", "成都", "北京", "天津", "沈阳", "武汉", "杭州", "深圳", "广州", "西安"]

        # 列表框+城市列表
        for city in cities:
            city_listbox.insert(tk.END, city)

        # 创建一个文本输入框，该输入框位于 city_window 子窗口中。
        search_entry = ttk.Entry(city_window)
        search_entry.pack(side="top", padx=5, pady=20)

        def filter_cities(event=None):
            # 获取搜索框中的文本，转换为小写
            search_term = search_entry.get().lower()
            # 清空城市列表框
            city_listbox.delete(0, tk.END)
            # 根据搜索关键字过滤并插入符合条件的城市
            for city in cities:
                if search_term in city.lower():
                    city_listbox.insert(tk.END, city)

        # 绑定搜索事件
        search_entry.bind("<KeyRelease>", filter_cities)

        def select_city(event=None):
            # 获取选中的城市名
            selected_city = city_listbox.get(city_listbox.curselection())
            # 赋值：全局变量
            GUI.CITY_NAME = selected_city
            # 清空输入框
            self.city_entry.delete(0, tk.END)
            # 插入输入框
            self.city_entry.insert(0, selected_city)
            # 关闭城市选择窗口
            city_window.destroy()

        # 绑定双击事件
        city_listbox.bind("<Double-Button-1>", select_city)

        # 创建确定按钮，点击时调用 select_city 函数
        select_button = ttk.Button(city_window, text="确定", command=select_city)
        select_button.pack(pady=10)

        # 初始时调用一次 filter_cities 函数，确保显示所有城市
        filter_cities()

    # 返回：城市名称
    @classmethod
    def get_city_name(cls):
        return cls.CITY_NAME

    # 返回：评论内容
    @classmethod
    def get_comment_content(cls):
        return cls.COMMENT_CONTENT

    # 返回：Cookie
    @classmethod
    def get_cookie(cls):
        return cls.COOKIE

    @classmethod
    def get_dp_cookie(cls):
        return cls.DP_COOKIE

    @classmethod
    def get_number(cls):
        return cls.NUMBER

    @classmethod
    def get_time(cls):
        return cls.TIME

    # 关闭GUI
    def start_comment(self):

        # 获取输入框中的城市名称
        entered_city = self.city_entry.get()
        # 如果城市名称为空
        if not entered_city:
            # 显示提示消息框
            messagebox.showinfo("提示", "请输入城市名称")
            # 结束函数，等待用户重新输入
            return
        # 赋值给类变量：CITY_NAME
        GUI.CITY_NAME = entered_city

        # 获取输入框中的评论内容
        entered_comment = self.comment_entry.get()
        # 如果评论内容为空
        if not entered_comment:
            # 显示提示消息框
            messagebox.showinfo("提示", "请输入评论内容")
            # 结束函数，等待用户重新输入
            return
        # 赋值给类变量：COMMENT_CONTENT
        GUI.COMMENT_CONTENT = entered_comment

        # 获取输入框中的Cookie
        entered_cookie = self.cookie_entry.get()
        # 如果评论内容为空
        if not entered_cookie:
            # 显示提示消息框
            messagebox.showinfo("提示", "请输入Cookie")
            # 结束函数，等待用户重新输入
            return
        # 赋值给类变量：COOKIE
        GUI.COOKIE = entered_cookie

        # entered_dp_cookie = self.dp_cookie_entry.get()
        # # 如果评论内容为空
        # if not entered_dp_cookie:
        #     # 显示提示消息框
        #     messagebox.showinfo("提示", "请输入Cookie2")
        #     # 结束函数，等待用户重新输入
        #     return
        # # 赋值给类变量：DP_COOKIE
        # GUI.DP_COOKIE = entered_dp_cookie

        entered_number = self.number_entry.get()
        # 如果评论内容为空
        if not entered_number:
            # 显示提示消息框
            messagebox.showinfo("提示", "请输入评论数量(单页)")
            # 结束函数，等待用户重新输入
            return
        # 赋值给类变量：NUMBER
        GUI.NUMBER = entered_number

        entered_time = self.time_entry.get()
        # 如果评论内容为空
        if not entered_time:
            # 显示提示消息框
            messagebox.showinfo("提示", "请输入单次评论间隔时间(单位：分)")
            # 结束函数，等待用户重新输入
            return
        # 赋值给类变量：TIME
        GUI.TIME = entered_time

        # 关闭 GUI
        self.root.destroy()
    # 结束程序
    def close_window(self):
        sys.exit()


class Comment:
    # 初始化
    def __init__(self):
        print('1、Initializing...')
        # 创建Chrome驱动实例
        self.driver = self.create_chrome_driver()

    # 运行
    def run(self, cityname, comment_content, cookie, dp_cookie, number, time):
        # 城市名
        area_name = cityname
        # 评论数
        comment_number = int(number)
        # 评论时间间隔
        comment_time = int(time)
        # 打开首页
        self.open_home_page(area_name)
        # 获取最大页码
        max_page = self.get_max_page_number()
        # 处理编码
        cookie_encoded = quote(cookie)
        # 发送评论
        self.send_comment(max_page, area_name, comment_content, cookie_encoded, cookie, comment_number, comment_time) # 最大页码，城市名，评论内容，首页cookie, 详情页cookie, 单次评论数

    # 创建Chrome驱动实例
    def create_chrome_driver(self):
        print('2、Create an instance of Chrome WebDriver')
        # 创建实例
        self.driver = webdriver.Chrome()
        return self.driver

    # 打开首页
    def open_home_page(self, area_name):
        print('3、open home page')
        # 打开[会员购]首页
        self.driver.get("https://show.bilibili.com/platform/home.html?from=pc_mall")
        # 隐式等待5秒
        self.driver.implicitly_wait(5)
        # 点击指定的城市
        self.driver.find_element(By.XPATH, f"//ul[@class='city-list']//li[contains(text(),'{area_name}')]").click()

    # 获取最大页码
    def get_max_page_number(self):
        # 显式等待10秒
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="pagination"]/span')))
        # 利用XPATH，获取最大页码
        max_page = self.driver.find_elements(By.XPATH, '//div[@class="pagination"]/span')[-1].text
        # 打印
        print('4、gets the maximum page number: ' + max_page)
        # 强转并返回
        return int(max_page)

    # 发送评论
    def send_comment(self, max_page, area_name, comment_content, cookie_encoded, cookie,comment_number,comment_time):
        # 获取数据-url
        get_url = ""
        # 获取数据-请求头
        get_headers = {
            # 'Cookie': "_uuid=10DCC61DD-6109B-15B9-6979-34D7D422DB4583717infoc; b_nut=1686464184; buvid3=835601B3-AED1-F4FA-47DA-0F32CE994CB984052infoc; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; rpdid=|(J|YJJu)mJm0J'uY)YRYRkJJ; buvid4=8F3BF17B-F861-6352-EC33-79F551D28A7A84052-023061114-TNlJn%2By0Jb1TrkK9bOvm%2Bg%3D%3D; hit-dyn-v2=1; hit-new-style-dyn=1; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; buvid_fp_plain=undefined; is-2022-channel=1; CURRENT_QUALITY=64; iflogin_when_web_push=1; bp_video_offset_398076353=874585955746447445; fingerprint=f60d388eead613e08701fe74f10b8afc; buvid_fp=f60d388eead613e08701fe74f10b8afc; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI3MzMwODUsImlhdCI6MTcwMjQ3MzgyNSwicGx0IjotMX0.vbqtFDrtIrZEgPQP_PgI3kinsUiXFm7cZMXhF4HmZUc; bili_ticket_expires=1702733025; SESSDATA=9d42800b%2C1718025914%2Cae78b%2Ac2CjD2OCJ2e9EoiLJ9KVWwLBLWwcqISGXvBnSXUg5XkTiYGmgg2JyghbDiAak-DsiCX7ISVlZzWHoyQjFfb2VwQjEzajZOdHUwdHNwcjJCTnBPb0d4MU5EZjJNY2tlWGh5T3R0MEVUcm5hR0JQQnF4ZURBLWE5aEtLQzI4eE0wZVpOY0FQdzJSZldnIIEC; bili_jct=5d51725f93c9b8914299d9a3805ed158; DedeUserID=3546592713902157; DedeUserID__ckMd5=6ac4aac64c104dde; enable_web_push=DISABLE; PVID=2; browser_resolution=1280-607; home_feed_column=4; Hm_lvt_909b6959dc6f6524ac44f7d42fc290db=1702472938,1702474990,1702550542,1702655803; sid=8cgzpvlu; bsource=search_baidu; deviceFingerprint=1003d52eb659e01e50e8d4647caa12d1; b_lsid=CA76552D_18C71453D14; msource=pc_web; from=pc_ticketlist",
            'Cookie': cookie_encoded,
            'Referer': 'https://show.bilibili.com/platform/home.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        # 城市编码
        city_codes = {
            "全国": "-1",
            "上海": "310100",
            "成都": "510100",
            "北京": "110100",
            "天津": "120100",
            "沈阳": "210100",
            "武汉": "420100",
            "杭州": "330100",
            "深圳": "440300",
            "广州": "440100"
        }
        # 获取对应的城市编码
        city_code = city_codes.get(area_name, None)
        # p_type 处理
        p_type_value = "全部类型"
        p_type_encoded = quote(p_type_value)
        # 发送数据-url
        post_url = "https://show.bilibili.com/api/ticket/comment/add"
        # 自动评论
        for number in range(1, max_page + 1):
            url = f'https://show.bilibili.com/api/ticket/project/listV2?version=134&page={number}&pagesize=16&area={city_code}&filter=&platform=web&p_type={p_type_encoded}'
            print(f"第{number}“”页: " + url)
            # 获取数据
            response = requests.get(url, headers=get_headers)
            if response.status_code == 200:
                # 解析 JSON 数据
                json_data = response.json()
                print('JSON：')
                print(json_data)
                # 遍历result列表
                for i in json_data['data']['result']:
                    print("5、go to details page")
                    # 获取id和project_name的值
                    id = i['id']
                    print(f"id: {id}")
                    project_name = i['project_name']
                    print(f"project_name：{project_name}")
                    # comment_number 单页评论次数
                    for j in range(comment_number):
                        # 子函数
                        def generate_random_chinese():
                            # 生成一个随机汉字
                            return chr(random.randint(0x4e00, 0x9fff))
                        # 生成5个随机汉字
                        for v in range(5):
                            random_chars = ''.join(generate_random_chinese() for _ in range(5))
                        print('随机码: ' + random_chars)
                        #sys.exit()

                        # cookie格式处理
                        # 将cookie字符串分割成键值对
                        cookie_pairs = cookie.split('; ')
                        # 创建一个字典来存储键值对
                        cookie_dict = {}
                        for pair in cookie_pairs:
                            key, value = pair.split('=')
                            cookie_dict[key.strip()] = value.strip()
                        # 格式化成标准的Cookie格式
                        formatted_cookie = "; ".join([f"{key}={value}" for key, value in cookie_dict.items()])

                        # 封装请求头
                        post_headers = {
                            #'Cookie': "_uuid=10DCC61DD-6109B-15B9-6979-34D7D422DB4583717infoc; b_nut=1686464184; buvid3=835601B3-AED1-F4FA-47DA-0F32CE994CB984052infoc; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; rpdid=|(J|YJJu)mJm0J'uY)YRYRkJJ; buvid4=8F3BF17B-F861-6352-EC33-79F551D28A7A84052-023061114-TNlJn%2By0Jb1TrkK9bOvm%2Bg%3D%3D; hit-dyn-v2=1; hit-new-style-dyn=1; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; buvid_fp_plain=undefined; is-2022-channel=1; CURRENT_QUALITY=64; iflogin_when_web_push=1; fingerprint=f60d388eead613e08701fe74f10b8afc; enable_web_push=DISABLE; home_feed_column=4; PVID=1; bp_video_offset_3546592713902157=880819525228953718; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDU0MDQyMTIsImlhdCI6MTcwNTE0NDk1MiwicGx0IjotMX0.RIYO7F6bsscu31pPJtWnHGrqhOoIiODzyzZ85--6X7E; bili_ticket_expires=1705404152; msource=pc_web; deviceFingerprint=1003d52eb659e01e50e8d4647caa12d1; Hm_lvt_909b6959dc6f6524ac44f7d42fc290db=1702907107,1702991995,1705065571,1705145079; bsource=search_baidu; from=pc_ticketlist; innersign=0; bp_video_offset_3546608971024595=0; browser_resolution=1280-607; b_lsid=44C10AE73_18D02E27905; buvid_fp=835601B3-AED1-F4FA-47DA-0F32CE994CB984052infoc; SESSDATA=485b395e%2C1720705723%2C63cbb%2A12CjAMsVgSy8I5yBY3Ut7T2hOQhsX5pBhJGdaNc5glePX8ygGpYdch44kGR6iB6C7cLaYSVl9oX3JORjdLYjltejVJaUJxQmdJSEZCU0N3REdKNWozNHZKRDYtQkNvd3V1UmRRTjFaSEJpWlBseUo1WENQdXVwalB1OTVNbG03LS1UZlhxUlRzX2xnIIEC; bili_jct=80a84e9ca9ac42d62ae4cd5e10558bc9; DedeUserID=3546608971024595; DedeUserID__ckMd5=13444936cbb1c60d; sid=8s9jdg93; Hm_lpvt_909b6959dc6f6524ac44f7d42fc290db=1705154372",
                            # 'Cookie': dp_cookie,
                            'Cookie': formatted_cookie,
                            'Origin': 'https://show.bilibili.com',
                            'Referer': f'https://show.bilibili.com/platform/detail.html?id={id}&from=pc_ticketlist',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        }
                        # 请求数据
                        comment_info = {
                            'content': comment_content + random_chars, # 评论内容
                            'subjectId': id, # 项目id
                            'subjectName': project_name, # 项目名称
                            'subjectType': '2'
                        }
                        # 发起POST请求
                        post_response = requests.post(url=post_url, headers=post_headers, data=comment_info)
                        # 解析 JSON 数据
                        post_json_data = post_response.json()
                        print(f"Result: {post_json_data}")
                        print("Msg：" + post_json_data['msg'])
                        if post_json_data['msg'] == '抱歉，只有离开了小黑屋才能写评论哦。':
                            print('提示：当前账号已被封，请切换账号再试！')
                            # 退出程序
                            sys.exit()
                        if post_json_data['msg'] == '请先登录':
                            print('提示：未登录，请登录账号后重试！')
                            # 退出程序
                            sys.exit()
                        if post_response.status_code == 200 and post_json_data['msg'] != '刚刚发布了相同的内容哦~':
                            print('提示：评论成功！')
                        else:
                            print(f"提示：评论失败： {post_response.status_code}")
                        # if post_json_data['msg'] != '' and post_json_data['msg'] == '刚刚发布了相同的内容哦~':
                        #     print('project_name: ' + project_name + '\n' + 'Msg：评论失败！' + '\n')
                        # # 判断评论是否成功
                        # if post_response.status_code == 200 and post_json_data['msg'] != '刚刚发布了相同的内容哦~':
                        #     print('project_name: ' + project_name + '\n' + 'Msg：评论成功！' + '\n')
                        # else:
                        #     print(f"post_response failed with status code {post_response.status_code}")
                        # 睡眠20秒
                        time.sleep(comment_time * 60)
                    # 睡眠20秒
                    time.sleep(20)
            else:
                print(f"get_response failed with status code {response.status_code}")
            # 睡眠20秒
            time.sleep(20)

if __name__ == '__main__':
    # 1、打开GUI界面，并配置好相关参数
    GUI().run()
    # 2、点击[开始评论]按钮，并开始进行"自动评论"
    Comment().run(GUI.get_city_name()
                  , GUI.get_comment_content()
                  , GUI.get_cookie()
                  , GUI.get_dp_cookie()
                  , GUI.get_number()
                  , GUI.get_time())