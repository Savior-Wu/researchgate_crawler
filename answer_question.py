#! -*- coding:utf-8 -*-

import requests
import json
import time
import re
from bs4 import BeautifulSoup as BS
from core.db_connect import db_connection as DB

class answer_question():

    def __init__(self):
        self.header = {
            "user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "cookie":"did=xoYKwaUr5JrZS8IuIIqLwcZOA0AvUdbGn1vIOjL2AJBldxmth2ZT236dmeXsyEMV; ptc=RG1.2473307923511623367.1541590117; _ga=GA1.2.1962697362.1541590119; _mkto_trk=id:931-FMK-151&token:_mch-researchgate.net-1541592868827-57337; __gads=ID=07241de65be85996:T=1544624077:S=ALNI_MaYekYEYaPg_KVoJYR1Y5bH36M_WA; _gid=GA1.2.628786030.1550404404; pl=XYmycGXpxnMPlpaD9DFMInmJDYlVDlc1x3O44CB5OMz00qbs2AfCIWz5zAPQOQH12CoZCkSFiO4fVn1hPWGQ0LE2Na1kUMXeVys60ooCON3JrDCy1FZYMSls7iT5DHow; sid=meykJ0DPjElHkR4UdJt7osKZg8CiJPk4C4CMf3FkndLiUCGbTVUEmHJVfmC0Zwq0wJtwV00NNj8CRyRlfLwNCwtHxlLG0wGbVLmj3yTpeAtijnqx1xKHaf72ltCsuCRv; cili=_2_YzE5NmI3YzMxYjExZGZiMDk0MTRhNjI5Y2NkOGVjNmQ3NGRlZTQ2MzhjYzBhMTM4ODhhNzQ3MzRlNDU0ZWI4M18xMTYzMTAwMzsw; cirgu=_1_gD0AnOouzggwabJAkZxaGadQhZVude4mz6%2FsTbxZEugjBPbfmK5WwVX%2Brx6nb%2BalfmpVVw%3D%3D; _gat=1"
        }

        self.base_url = "https://www.researchgate.net/"

    def answer_single(self,person):
        # get token in answers
        answer_url = self.base_url + str(person) + '/answers'
        req = requests.get(answer_url, headers = self.header)
        soup = BS(req.text,'lxml')
        first_token_label = soup.find("meta", id="Rg-Request-Token")
        first_token = first_token_label.get("content")
        account_info = DB().query_exists_account_info(str(person))
        if account_info:
            # query return tuples, each tuple contains two values
            accountid = account_info[0][0]
            accountkey = account_info[0][1]
        else:
            accountid = re.search(r'("profileAccountId":)(\d+)(,)',str(req.text), re.M).group(2)
            accountkey = re.search(r'("profileAccountKey":")(\w+)(",)',str(req.text), re.M).group(2)
            DB().insert_account_info((str(person),accountid,accountkey))

        # get token after answers request
        tmp_headers = self.header
        tmp_headers["referer"] = answer_url
        tmp_headers["rg-request-token"] = first_token
        tmp_headers["accept"] = "applicaiton/json"
        print(first_token)
        # tmp_headers["origin"] = "https://www.researchgate.net"
        ProfileAnswerPostList = "https://www.researchgate.net/profile.ProfileAnswerPostList.html?accountId={}&profileAccountKey={}".format(accountid, accountkey)
        print(ProfileAnswerPostList)
        req_2 = requests.get(ProfileAnswerPostList, headers = tmp_headers)
        rg_request_token = re.search(r'(id="Rg-Request-Token" content=")(\S+)(")',str(req_2.text), re.M).group(2)
        print(rg_request_token)

        # get data
        data_header = tmp_headers
        data_header["rg-request-token"] = rg_request_token
        data_header["accept"] = "application/json"
        data_header["origin"] = "https://www.researchgate.net"
        data_header["content-type"] = "application/json"

        answer_data_url = "https://www.researchgate.net/graphapi/9k7idy"
        json_id = "AC:{}".format(accountid)
        json_data = {"queryName":"ProfileAnswerPostList","variables":{"offset": 630, "limit": 121, "id": json_id}}
        # print(json_data)
        req_data = requests.post(answer_data_url, headers = data_header ,json=json_data)
        print(req_data.json()["result"]["data"]["account"]["latestAuthoredAnswerPosts"])

        with open("../source_data/data.json",'w+') as f:
            f.write(str(req_data.json()))



if __name__ == "__main__":
    answer_question().answer_single('profile/SN_Piramanayagam')

