#! -*- coding:utf-8 -*-

import requests
import copy
import time
from lxml import etree
from bs4 import BeautifulSoup as BS
from core.db_connect import db_connection as db_conn

class researchgate_get():
    def __init__(self):
        self.header = {
            "user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "cookie":"cookie"
        }
        # https: // www.researchgate.net / institution / Wuhan_University / members
        # self.url = 'https://www.researchgate.net/institution/Wuhan_University/members'

    # def req_researchgate(self):
    #     req = requests.get(self.url, headers = self.header)
    #     return req

    def req_researchgate(self,mem_url):
        req = requests.get(mem_url, headers = self.header)
        return req

class members_data():
    def __init__(self):
        self.base_url = 'https://www.researchgate.net/institution/'

    def all_url(self):
        return
    def get_all_ul(self, req):
        soup = BS(req.text,'lxml')
        return soup.find_all('ul', class_ = 'list people-list-m')

    def get_all(self, req):
        mem_dict = {}
        mem_list =[]
        mem_dict_tmp = {}
        soup = self.get_all_ul(req)
        uni_name = []
        dep_name = []
        influ_score = {}

        # each page has 25 members
        for li in soup:
            image = li.select('li > div > div > a > img')
            profile = li.select('li > div > h5 > a')
            university = li.select('li > div[class="indent-content"] > div')
            # print(university.get_text())
            for i in range(len(university)):
                # extract university name and department name
                if i % 2 == 0 :
                    uni_dep = university[i].get_text()
                    if '·' not in uni_dep:
                        uni_name.append(str(uni_dep).strip())
                        dep_name.append('')
                        continue
                    # print(uni_dep)
                    uni_name.append(uni_dep.split('·')[0].strip())
                    dep_name.append(uni_dep.split('·')[1].strip())

            # get influence score
            influence = li.select('li > div > h5 > span > span > div > div > a')
            for i in influence:
                # print(i)
                score_href = i.get('href')
                influ_score[score_href[0:(len(score_href)-7)]] = i.get_text()
                # print(influ_score)

            # replace spacial character
            for i in range(len(dep_name)):
                if '\u3000' in dep_name[i]:
                    dep_name[i] = dep_name[i].replace('\u3000',' ')

            # print(len(dep_name))

            for i in range(len(image)):
                mem_dict['image'] = image[i].get('data-src')
                mem_dict['profile'] = profile[i].get('href')
                mem_dict['name'] = profile[i].get_text()
                mem_dict['university'] = uni_name[i]
                mem_dict['department'] = dep_name[i]
                if mem_dict['profile'] in influ_score.keys():
                    mem_dict['influence_score'] = float(influ_score[mem_dict['profile']])
                else:
                    mem_dict['influence_score'] = 0
                # print(mem_dict)
                mem_list.append(copy.deepcopy(mem_dict))
        return mem_list

    # calculation page numbers by members
    def get_pages(self, req):
        html = etree.HTML(req.text)
        members = html.xpath("//h2/text()")[0]
        page = int(int(members[9:(len(members)-1)])/25+1)
        # print(page)
        return page

    # insert into database of one page
    def insert_one_page(self, req, university_tbname):
        origin_dict = self.get_all(req)
        tmp_list = []
        for i in origin_dict:
            for j in i.values():
                tmp_list.append(j)
            # print(tmp_list)
            # insert with scores
            if tmp_list[-1] >0:
                db_conn().db_insert_university(tuple(tmp_list),str(university_tbname))
            tmp_list.clear()

    # insert into database

    #
    def read_data(self):
        university_tuple = db_conn().read_university()
        for univer in range(0,len(university_tuple)):
            url = self.base_url + str(university_tuple[univer]) + '/members'
            university_tbname = 'oringin_table_' + str(university_tuple[univer])
            req_status = 0
            req = None
            try:
                req = researchgate_get().req_researchgate(url)
                req_status=req.status_code
            except Exception as e:
                print('[page calculation]connection error : %s' % e)
            while (req_status !=200 ):
                try:
                    req = researchgate_get().req_researchgate(url)
                    req_status = req.status_code
                except Exception as e:
                    print('[page calculation]connect error : %s' % e)
                    time.sleep(30)
                    print('[page calculation] connect try again...')
            page = self.get_pages(req)
            for i in range(int(page)):
                # if i%23 == 0:
                #     time.sleep(5)
                req_page =None
                status_code=0
                try:
                    req_page = researchgate_get().req_researchgate(url + '?page=' + str(i+1))
                    status_code = req_page.status_code
                except Exception as e:
                    print('connection error firstly: %s' %e)
                while (status_code != 200):
                    try:
                        req_page = researchgate_get().req_researchgate(url + '?page=' + str(i + 1))
                        status_code = req_page.status_code
                    except Exception as e:
                        print('Error:%s'%e)
                        time.sleep(45)
                        print('try again...')
                time.sleep(3)
                print('university: %s [%s]insert page %d start...' %(university_tuple[univer], time.strftime('%Y-%m-%d %H:%M:%S'),i+1))
                self.insert_one_page(req_page, university_tbname)
                print('university: %s [%s]insert page %d end...' %(university_tuple[univer], time.strftime('%Y-%m-%d %H:%M:%S'),i+1))
                # time.sleep(2)

if __name__ == "__main__":
    members_data().read_data()
