from selenium import webdriver
import logging
import time
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from retrying import retry
from selenium.webdriver import ActionChains


#用logging模块查看错误日志
logging.basicConfig(level=logging.INFO,format='%(asction)s-%(name)s-%(levelname)s-%(message)s')
logger = logging.getLogger(__name__)

class taobao():
    def __init__(self):
        self.browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        # 最大化窗口
        self.browser.maximize_window()
        self.browser.implicitly_wait(5)
        self.domain = 'http://www.taobao.com'
        self.action_chains = ActionChains(self.browser)

    def login(self, username, password):
        while True:
            self.browser.get(self.domain)
            time.sleep(1)

            #点击“请登录”按钮
            self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul[1]/li[2]/div[1]/div[1]/a[1]').click()
            #输入用户名
            self.browser.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
            #输入密码
            self.browser.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
            time.sleep(1)

            try:
                # 出现验证码，滑块验证
                slider = self.browser.find_element_by_xpath("//span[contains(@class, 'btn_slide')]")
                #滑块不是每次都出现，要yongif语句判断
                if slider.is_displayed():
                    #拖拽滑块
                    self.action_chains.drag_and_drop_by_offset(slider,258,0).perform()
                    time.sleep(0.5)
                    #释放滑块，相当于点击拖拽之后的释放鼠标
                    self.action_chains.release().perform()
            except(NoSuchElementException, WebDriverException):
                logger.info('未出现登录验证码')

            #点击登录按钮
            self.browser.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div[1]/div/div[2]/div/form/div[4]/button').click()

            nickname = self.get_nickname()
            if nickname:
                logger.info('登录成功，昵称为'+nickname)
                break
            logger.debug('登录出错，5s后继续登录')
            time.sleep(5)

    #返回用户名
    def get_nickname(self):
        self.browser.get(self.domain)
        time.sleep(0.5)
        try:
            return self.browser.find_element_by_class_name('site-nav-user').text
        except NoSuchElementException:
            return ''

if __name__ == '__main__':
    #填写用户名和密码
    username = ''
    password = ''
    tb = taobao()
    tb.login(username,password)
