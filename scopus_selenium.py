#! -*- coding:utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup as BS
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.db_connect import db_connection as DB

class scopus_selenium():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.first_name = '//div[@class="form-group"]/span/label[@for="firstname"]'
        self.last_name = '//div[@class="form-group"]/span/label[@for="lastname"]'
        self.university = '//div[@class="form-group"]/span/label[@for="institute"]'
        self.exact = '//div[@class="col-md-4"]/input[@id="exactSearch"]'
        self.submit = '//div[@class="col-md-2"]/button[@id="authorSubmitBtn"]'
        self.driver.maximize_window()
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "cache-control": "max-age=0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "cookie": '__cfduid=d0a741ad4e2dd6432bee717e0e20e2a081551612544; optimizelyEndUserId=oeu1551612544971r0.7714426673811274; scopusSessionUUID=07c3f98d-a04c-4d6f-b; NEW_AE_SESSION_COOKIE=1551612549765; scopus.machineID=2E56B4536198C563A66FC917D356C5C9.wsnAw8kcdt7IPYLO0V48gA; screenInfo="1080:1920"; NEW_CARS_COOKIE=0033006600680057006F0055003400580051006D006E0062006B005800790072005A0079003400360043005700340072004200330071005400520066006C0070004300730044004B00610057006200520052004E006F00460032007700730050005300670070005600540064003500560043004200410057004A00340036007700540062004B0079007A00710048006A0041006300540071006E00620073002B006C0037003600420056007200760036006D00720055005A00380058004C006C0052005600610075004C006A0041006200780050004400560045004C006B006E006400760038007900590059005000730042004D007300390054004100790074; SCSessionID=DE1D341DAEDF73CF3435BA31E1464E49.wsnAw8kcdt7IPYLO0V48gA; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1201F8B2BE10C09CB16BF80CE887F5621ACE5E261E332BE227C298BBA919F55FB10BA32070D9964CEACBAE7C5777723B7553B284D344502B02EEAA0BC080A53A3; __cfruid=cf317dda6b8e7b952fd7e91007350417c3cf761c-1551612551; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22direct%22%7D; javaScript=true; _pk_ses.2316.d989=*; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; _pendo_accountId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A278641; _pendo_visitorId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A37822685; _pendo_meta.7108b796-60e0-44bd-6a6b-7313c4a99c35=2930597497; xmlHttpRequest=true; optimizelyBuckets=%7B%2212850330201%22%3A%2212837340081%22%7D; _pk_id.2316.d989=2b16213d9afd9cbe.1551612553.1.1551615214.1551612553.; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-330454231%7CMCIDTS%7C17959%7CMCMID%7C41325088313242409931101817438408090608%7CMCAAMLH-1552220015%7C9%7CMCAAMB-1552220015%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1551619753s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17966%7CMCCIDH%7C-164432718%7CvVersion%7C3.1.2; s_pers=%20c19%3Dsc%253Arecord%253Aauthor%2520details%7C1551617015693%3B%20v68%3D1551615214342%7C1551617015711%3B%20v8%3D1551615226445%7C1646223226445%3B%20v8_s%3DFirst%2520Visit%7C1551617026445%3B; optimizelyPendingLogEvents=%5B%5D; s_sess=%20s_cpc%3D0%3B%20c21%3Dlastname%253Djian%2526firstname%253Dli%3B%20e13%3Dlastname%253Djian%2526firstname%253Dli%253A1%3B%20c13%3Ddocument%2520count%2520%2528high-low%2529%3B%20s_sq%3D%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Aauthor%252520results%252C60%252C60%252C938%252C1920%252C938%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dsc%25253Arecord%25253Aauthor%252520details%252C50%252C50%252C938%252C1119%252C938%252C1920%252C1080%252C1%252CP%3B'
        }

    def single(self, data):
        first_name = data[0]
        last_name = data[1]
        university = data[2]

        person_data = []

        self.driver.get("https://www.scopus.com/freelookup/form/author.uri?zone=&origin=searchauthorfreelookup")
        time.sleep(3)
        # tmp_page_source = self.driver.page_source
        # web_status = 'loading'
        # while web_status != 'complete':
        #     time.sleep(0.5)
        #     web_status = self.driver.execute_script('document.readyState')
        web_page_source = self.driver.page_source
        last = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,self.last_name)))
        last.click()
        # last = self.driver.find_element_by_xpath(self.last_name).click()
        try:
            last.clear()
            print('clear')
        except:
            print('no clear')
        # last.send_keys(last_name)
        for i in last_name:
            self.driver.switch_to.active_element.send_keys(i)
        time.sleep(0.5)
        # last = self.driver.find_element_by_xpath(self.last_name).click()
        first = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.first_name)))
        first.click()
        # first.clear().send_keys(first_name)
        try:
            first.clear()
            print('clear')
        except:
            print('no clear')
        # first.send_keys(first_name)
        for i in first_name:
            self.driver.switch_to.active_element.send_keys(i)
        time.sleep(0.5)
        # univ = self.driver.find_element_by_xpath(self.university).click()
        univ = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.university)))
        univ.click()
        # univ.clear().send_keys(university)
        try:
            univ.clear()
            print('clear')
        except:
            print('no clear')
        # univ.send_keys(university)
        for i in university:
            self.driver.switch_to.active_element.send_keys(i)
        time.sleep(0.5)
        self.driver.find_element_by_id('exactSearchCheck').click()
        self.driver.find_element_by_xpath(self.submit).click()
        time.sleep(2)

        # while web_status != 'complete':
        #     time.sleep(0.5)
        #     web_status = self.driver.execute_script('document.readyState')

        page_source = self.driver.page_source
        for i in range(6):
            if page_source == web_page_source:
                time.sleep(5)
            elif i == 5:
                curr_data = []
                curr_data.extend([first_name, last_name, university])
                return self.single(curr_data)
            else:
                break

        soup = BS(page_source, 'lxml')
        data_row_source = soup.find('tr', attrs={'id':'resultDataRow1'})
        data_row = []
        for i in data_row_source[0].get_text():
            data_row.append(i)

        h_index = 0
        author_out = 0
        author_quote = 0

        if (','.join([last_name,first_name]) or ', '.join([last_name,first_name]) in data_row) and university in data_row:
            person_url = data_row_source[0].select('td > a ')[0].get('href')
        else:
            person_url = None
            person_data.extend([h_index, author_out, author_quote])
            return person_data

        person_page_status = None
        while(person_page_status):
            try:
                person_page = requests.get(person_url, headers = self.headers)
                person_page_status = person_page.status_code
            except Exception as e:
                print('request failed:%s'%e)
                time.sleep(15)
                print('request again...')

        person_data_all = soup.select(' section[class="row"] > div[2] > section')
        for i in range(len(person_data_all)):
            if i == 1:
                h_index = etree.HTML(person_data_all[i]).xpath('//div[@class="panel-body]/span/text()')
                # h_index = person_data_all[i].find('div', attrs={'class':'panel-body'}).get_text()
            elif i == 2:
                author_out = etree.HTML(person_data_all[i]).xpath('//div[@class="panel-body"]/span/text()')
                # author_out = person_data_all[i].select('div[@class="panel-body] > span').get_text()
            elif i == 3:
                author_quote = etree.HTML(person_data_all[i]).xpath('//div[@class="panel-body"]/span[@class="lightGreyText"]/button/span[@id="totalCiteCount"]/text()')
            else:
                continue

        person_data.extend([h_index,author_out,author_quote])
        return person_data

    def read_persons(self):
        persons_data = DB().query_name_university()
        return persons_data

    def insert_data(self, data):
        DB().insert_scopus_data(data)

    def run(self):
        persons_data = self.read_persons()
        for person_data in persons_data:
            insert_data = []
            insert_data.extend(person_data)

            deal_person_data = []
            last_name = str(person_data[1]).split(' ')[-1]
            first_name = str(person_data[1]).split(' ')[:-1:]
            university = person_data[2]
            deal_person_data.extend([first_name, last_name, university])

            print("[{}] deal data start:{}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), person_data[0]))
            person_paper_data = self.single(deal_person_data)
            print("[{}] deal data end:{}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), person_data[0]))

            insert_data.extend(person_paper_data)

            print('insert data begin:%s' % person_data[0])
            # self.insert_data(insert_data)
            print('insert data end:%s' % person_data[0])

            print(insert_data)

        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    scopus_selenium().run()