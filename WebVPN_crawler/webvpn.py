from os import access
from selenium.webdriver.remote.webdriver import WebDriver as wd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
import selenium
from bs4 import BeautifulSoup as BS
import json

class WebVPN:
    def __init__(self, opt: dict, headless=False):
        self.root_handle = None
        self.driver: wd = None
        self.passwd = opt["password"]
        self.userid = opt["username"]
        self.headless = headless

    def login_webvpn(self):
        """
        Log in to WebVPN with the account specified in `self.userid` and `self.passwd`

        :return:
        """
        d = self.driver
        if d is not None:
            d.close()
        d = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        d.get("https://webvpn.tsinghua.edu.cn/login")
        username = d.find_elements(By.XPATH,
                                   '//div[@class="login-form-item"]//input'
                                   )[0]
        password = d.find_elements(By.XPATH,
                                   '//div[@class="login-form-item password-field" and not(@id="captcha-wrap")]//input'
                                   )[0]
        username.send_keys(str(self.userid))
        password.send_keys(self.passwd)
        d.find_element(By.ID, "login").click()
        self.root_handle = d.current_window_handle
        self.driver = d
        return d

    def access(self, url_input):
        """
        Jump to the target URL in WebVPN

        :param url_input: target URL
        :return:
        """
        d = self.driver
        url = By.ID, "quick-access-input"
        btn = By.ID, "go"
        wdw(d, 50).until(EC.visibility_of_element_located(url))
        actions = AC(d)
        actions.move_to_element(d.find_element(*url))
        actions.click()
        actions.\
            key_down(Keys.CONTROL).\
            send_keys("A").\
            key_up(Keys.CONTROL).\
            send_keys(Keys.DELETE).\
            perform()
        d.find_element(*url)
        d.find_element(*url).send_keys(url_input)
        d.find_element(*btn).click()

    def switch_another(self):
        """
        If there are only 2 windows handles, switch to the other one

        :return:
        """
        d = self.driver
        assert len(d.window_handles) == 2
        wdw(d, 50).until(EC.number_of_windows_to_be(2))
        for window_handle in d.window_handles:
            if window_handle != d.current_window_handle:
                d.switch_to.window(window_handle)
                return

    def to_root(self):
        """
        Switch to the home page of WebVPN

        :return:
        """
        self.driver.switch_to.window(self.root_handle)

    def close_all(self):
        """
        Close all window handles

        :return:
        """
        while True:
            try:
                l = len(self.driver.window_handles)
                if l == 0:
                    break
            except selenium.common.exceptions.InvalidSessionIdException:
                return
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()

    def login_info(self):
        """
        TODO: After successfully logged into WebVPN, login to info.tsinghua.edu.cn

        :return:
        """
        element_username = By.NAME, 'userName'
        element_password = By.NAME, 'password'
        self.access('info.tsinghua.edu.cn')
        self.switch_another()
        d = self.driver
        wdw(d, 50).until(EC.visibility_of_element_located(element_username))
        d.find_element(*element_username).send_keys(self.userid)
        d.find_element(*element_password).send_keys(self.passwd)
        element_input = By.XPATH, '//td[@class="but"]/input'
        d.find_elements(*element_input)[0].click()
        wdw(d, 30).until(EC.visibility_of_element_located((By.ID, 'menu')))
        # Hint: - Use `access` method to jump to info.tsinghua.edu.cn
        #       - Use `switch_another` method to change the window handle
        #       - Wait until the elements are ready, then preform your actions
        #       - Before return, make sure that you have logged in successfully
        #raise NotImplementedError

    def get_grades(self):
        """
        TODO: Get and calculate the GPA for each semester.

        Example return / print:
            2020-秋: *.**
            2021-春: *.**
            2021-夏: *.**
            2021-秋: *.**
            2022-春: *.**

        :return:
        """
        d = self.driver
        """
        element_gpa_url = By.XPATH, '/html/body/div[2]/div[1]/table/tbody/tr/td[1]/div/div/ul/li[2]/div[6]/div[3]/div/dl/dt[2]/a'
        wdw(d, 50).until(EC.visibility_of_element_located(element_gpa_url))
        d.find_element(*element_gpa_url).click()
        d.switch_to.window(d.window_handles[2])
        """
        d.close()
        self.to_root()
        self.access('zhjw.cic.tsinghua.edu.cn/cj.cjCjbAll.do?m=bks_cjdcx&cjdlx=zw')
        self.switch_another()
        element_gpa_info = By.XPATH, '/html/body/center/table[2]/tbody'
        gpa_info_html = d.find_element(*element_gpa_info)
        gpa_soup = BS(gpa_info_html.get_attribute('innerHTML'), 'lxml')
        gpa_table = gpa_soup.find_all('tr')
        gpa_info = []
        for index, row in enumerate(gpa_table):
            if index:
                tmp = row.find_all('td')
                gpa_info.append({   
                    'credit': tmp[2].text.strip(),
                    'gpa': tmp[4].text.strip(),
                    'semester': tmp[5].text.strip()
                })
        gpa_total = {}
        credit_total = {}
        gpa_avg = {}
        for course in gpa_info:
            if course['gpa'] == 'N/A':
                pass
            else:
                seme = course['semester']
                if seme in gpa_total:
                    gpa_total[seme] += (float(course['gpa']) * int(course['credit']))
                else:
                    gpa_total[seme] = (float(course['gpa']) * int(course['credit']))
                if seme in credit_total:
                    credit_total[seme] += int(course['credit'])
                else:
                    credit_total[seme] = int(course['credit'])
        for seme in gpa_total:
            gpa_avg[seme] = gpa_total[seme] / credit_total[seme]
        for seme in gpa_avg:
            print(f'{seme}: ' + '%.2f' %(gpa_avg[seme]))
        # Hint: - You can directly switch into
        #         `zhjw.cic.tsinghua.edu.cn/cj.cjCjbAll.do?m=bks_cjdcx&cjdlx=zw`
        #         after logged in
        #       - You can use Beautiful Soup to parse the HTML content or use
        #         XPath directly to get the contents
        #       - You can use `element.get_attribute("innerHTML")` to get its
        #         HTML code

        #raise NotImplementedError

if __name__ == "__main__":
    # TODO: Write your own query process
    with open('settings.json', 'r') as f:
        gpa_calc = WebVPN(json.load(f))
    gpa_calc.login_webvpn()
    gpa_calc.login_info()
    gpa_calc.get_grades()
    gpa_calc.close_all()
    #raise NotImplementedError