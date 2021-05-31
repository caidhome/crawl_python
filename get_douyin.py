from appium import webdriver
from time import sleep
import win32con
import win32clipboard as w
import re
import requests
import random
import pyperclip
import xlwt
import xlrd
import csv
from xlutils.copy import copy
from datetime import datetime

class Action():
    def __init__(self):
        # 初始化配置，设置Desired Capabilities参数
        self.desired_caps = {
          "platformName": "Android",
          "deviceName": "SM-G977N",
          "appPackage": "com.ss.android.ugc.aweme",
          "appActivity": ".splash.SplashActivity",
          'automationName': 'UiAutomator1',
          'noReset': "False"
        }
        self.server = 'http://localhost:4723/wd/hub'
        self.driver = webdriver.Remote(self.server, self.desired_caps)
        self.start_x = 500
        self.start_y = 1000
        self.distance = 600 
    def comments(self):
        sleep(10)
        self.driver.tap([(500, 1200)], 500) 

    def scroll(self): 
        err_num = 0
        restart_num = 0
        res_file = 'urls.csv'
        with open(res_file, 'r', encoding='gbk', newline='', errors='ignore') as nfile:
            reader = csv.reader(nfile)
            nums = int(list(reader)[-1][0])+1
        
        is_one = True
        repeat_num = 1
        # 升级提醒
        flag = True
        max_err = 15
        max_repeat = 10
        while True:
            if err_num > max_err or repeat_num > max_repeat:
                restart_num = restart_num + 1
                print('\n\n第 %d 次重启: %s \n starting......' % (restart_num, datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')))
                sleep(2)
                self.driver.quit()
                sleep(5)
                self.driver = webdriver.Remote(self.server, self.desired_caps)
                sleep(10)
                print('重启结束: %s ended\n\n' % datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'))
                repeat_num = 0
                err_num = 0
                flag = True
            x = self.driver.get_window_size()['width']
            y = self.driver.get_window_size()['height']
            sleep(10)
            # print('wake5')
            while True:
                print('当前时间: %s ' % datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'))
                if err_num > max_err or repeat_num > max_repeat:
                    break   
                num_one_to_ten = random.randint(1,10)
                num_one_to_three = random.randint(1,3)
                num_one_to_ten2 = random.randint(1,10)
                num_ten_to_twenty = random.randint(10,20)
                # 正负10 以内随机数
                pn_num1 = 10 - random.randint(1,20)
                pn_num2 = 10 - random.randint(1,20)
                time_num = random.randint(1,3)
                big_num = random.randint(50,100)
                count = 0
                max_swip = 2
                while True:
                    sleep(2)
                    if is_one:
                        sleep(4)
                        is_one = False
                    # print('oper')
                    count = count+1
                    if count >= max_swip:
                        break
                    try:
                        self.driver.swipe(self.start_x + pn_num1, self.start_y + pn_num1, self.start_x+pn_num2,
                        self.start_y-self.distance+pn_num2, 500+pn_num2)
                    except Exception as es:
                        err_num = err_num+1
                        print('\n[ swipe1 ]报错了(%d)：%s \n' % (err_num, es))
                        continue
                sleep(time_num)
                print('\n*********第 %d 个 *********' % nums, )

                try:
                    share_btn = self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/icd")
                    
                    share_btn.click()
                except Exception as ex:
                    err_num = err_num+1
                    print('\n[分享点击] 报错(%d), %s \n' % (err_num, ex))
                    self.driver.press_keycode(4)
                    # nums = nums - 1
                    continue    
                sleep(2)
                try:
                    self.driver.swipe(569, 1182, 220, 1182, 500)
                except Exception as ex:
                    err_num = err_num+1
                    print('\n [ 分享滑动 ]报错(%d), %s \n' % (err_num, ex))
                    self.driver.press_keycode(4)
                    # nums = nums - 1
                    continue
                sleep(1.5)
                try:
                    self.driver.tap([(419, 1180)], 500)
                except Exception as ex:
                    err_num = err_num+1
                    print('[ 点击复制 ]链接报错(%d), %s' % (err_num, ex))
                    self.driver.press_keycode(4)
                    # nums = nums - 1
                    continue
                sleep(1.5)
                get_url_str = pyperclip.paste()
                print(get_url_str)
                pre_re_obj = re.search(r'[a-zA-Z][a-zA-Z]:/ (.+?)(https://v.douyin.com/(.+?)/)', get_url_str)
                if pre_re_obj:
                    pre_commit = pre_re_obj[1]
                    pre_url = pre_re_obj[2]
              # print('------- %s ---------'%pre_re_obj[1])
                    print('\nThe url of past by re is : %s\n' % pre_url)
                    try:
                        resp_url = requests.get(pre_url).url
                    except Exception as e:
                        err_num = err_num+1
                        print('[ 重定向 ]报错(%d), %s'% (err_num, e))
                        # print('重定向失败')
                        resp_url = '=====error======='
                        continue

                    try:
                        item_list = [nums, pre_url, resp_url, pre_commit]
                        
                        with open(res_file, 'a+', encoding='gbk', newline='', errors='ignore') as csvfile:
                            writer = csv.writer(csvfile)
                            with open(res_file, 'r', encoding='gbk', newline='', errors='ignore') as rfile:
                                reader = csv.reader(rfile)
                                # cur_list = [row for row in reader]
                                write_flag = True
                                for e_row in reader:
                                    if pre_commit in e_row or pre_url in e_row or resp_url in e_row:
                                        write_flag = False
                                        break
                                if write_flag:
                                    writer.writerow(item_list)
                                else:
                                    print('重复第 %d 次' % repeat_num)
                                    repeat_num = repeat_num + 1
                                    continue

                    except Exception as e:
                        err_num = err_num+1
                        print('[ 写入文件 ]报错(%d), %s'% (err_num, e))
                        continue         
                else:
                    print('[ 正则匹配 ]失败！')
                    continue
                nums = nums + 1

    def main(self):
        self.comments()
        self.scroll()
        
        
if __name__ == '__main__':
    action = Action()
    action.main()
