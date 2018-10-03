# coding=utf-8
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
import os
import sys
import Utf8

class Douyu:
    def __init__(self,G=False,username=u'',password=''):
        if G:
            self.browser = webdriver.Chrome()
        else:
            _chrome_options = webdriver.ChromeOptions()
            _chrome_options.add_argument('--headless')
            self.browser = webdriver.Chrome(chrome_options=_chrome_options)
        self.username = username
        self.password = password
    def _login(self):

        if os.path.exists('./cookie.json'):
            self.infoCookie()
        else:
            self.infoUserPass()

    def infoUserPass(self):
        self.browser.get("https://www.douyu.com/directory/myFollow")
        while (True):
            time.sleep(2)
            print self.browser.current_url
            self.browser.switch_to_frame("login-passport-frame")
            self.browser.find_element_by_class_name('scanicon-toLogin').click()
            time.sleep(1)
            self.browser.find_element_by_xpath('//*[@id="loginbox"]/div[3]/div[2]/div[2]/div[1]/span[3]').click()
            self.browser.find_element_by_xpath(
                '//*[@id="loginbox"]/div[3]/div[2]/div[2]/form/div[2]/div/input').send_keys(self.username)
            self.browser.find_element_by_xpath(
                '//*[@id="loginbox"]/div[3]/div[2]/div[2]/form/div[3]/input[1]').send_keys(self.password)
            time.sleep(1)
            self.browser.find_element_by_class_name('geetest_radar_tip').click()
            while (True):
                if 'PHPSESSID' in str(self.browser.get_cookies()):
                    print 'login success'
                    _cookie = self.browser.get_cookies()
                    self._keepCookie(_cookie)
                    break
            break

    def _keepCookie(self, cookies):
        print 'keeping cookie'
        fp = open('cookie.json', 'w')
        json.dump(cookies, fp)
        fp.close()

    def infoCookie(self):
        print 'exists cookie , loading ... '
        fp = open('cookie.json', 'r')
        cookies = json.load(fp)
        fp.close()
        self.browser.get("https://www.douyu.com")
        for cookie in cookies:
            self.browser.add_cookie(cookie)
        time.sleep(0.5)
        self.browser.refresh()
        if 'acf_nickname' in str(self.browser.get_cookies()):
            print 'login success'

    def _switchRoom(self,rooms,num=1):
        for room in rooms:
            self.browser.get("https://www.douyu.com/"+str(room))
            D._send(num)

    def _send(self,num):
        i = 1
        text = raw_input("input text : ")
        while (i<=num):
            try:
                self.browser.find_element_by_class_name("cs-textarea").click()
                # print text.encode('unicode_escape').decode('unicode_escape')
                # continue
                self.browser.find_element_by_class_name("cs-textarea").send_keys('No.'+str(i)+' : '+text.encode('unicode_escape').decode('unicode_escape'))
                mouse_ele = self.browser.find_element_by_class_name("b-btn")
                sleep_time = self.browser.find_element_by_class_name("b-btn").text
                # print 'sleep_time ' + str(sleep_time)
                if str.isalnum(str(sleep_time)):
                    st = int(sleep_time)
                else:
                    st = 1
                ActionChains(self.browser).move_to_element(mouse_ele).perform()
                print 'sending data : ' + 'No.'+str(i)+' : '+text.encode('unicode_escape').decode('unicode_escape')
                print u'系统休眠 ' + str(st)
                time.sleep(st)
                mouse_ele.click()
                print ' ok '
                # time.sleep(1)
            except Exception, e:
                print str(e)
            i = i + 1


if __name__ == '__main__':
    username = u''
    password = ''
    D = Douyu(G=True,username=username,password=password)
    D._login()
    rooms = ['5450787']
    D._switchRoom(rooms,num=100)

    # testcookie()
    print 'byby'
    D.browser.close()