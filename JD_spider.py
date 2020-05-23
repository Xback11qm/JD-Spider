from selenium import webdriver

import  time
import pymongo

class JdSpider:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.get('https://www.jd.com/')
        self.conn = pymongo.MongoClient('localhost',27017)
        self.db = self.conn['Jddb']
        self.myset = self.db['Jdset']

    def get_html(self):
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('爬虫书')
        self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        time.sleep(1)

    def parse_one_page(self):
        self.browser.execute_script( 'window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
        for li in li_list:
            item = {}
            item['name'] = li.find_element_by_xpath('.//div[@class="p-name"]/a/em').text.strip()
            item['price'] = li.find_element_by_xpath('.//div[@class="p-price"]/strong').text.strip()
            item['commit'] = li.find_element_by_xpath('.//div[@class="p-commit"]/strong').text.strip()
            item['shop'] = li.find_element_by_xpath('.//div[@class="p-shopnum"]').text.strip()
            print(item)
            self.myset.insert_one(item)

    def run(self):
        self.get_html()
        while True:
            self.parse_one_page()
            if self.browser.page_source.find('pn-next disabled') == -1:
                self.browser.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]').click()
                time.sleep(1)
            else:
                self.browser.quit()
                break

if __name__ == '__main__':
    spider =JdSpider()
    spider.run()