#! -*- coding:utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup as BS
from lxml import etree

class scopus_req():

    def __init__(self):
        self.search_author_url = 'https://www.scopus.com/freelookup/form/author.uri?zone=&origin=NO%20ORIGIN%20DEFINED'
        self.search_submit = 'https://www.scopus.com/search/submit/authorFreeLookup.uri'
        self.headers = {
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "cache-control":"max-age=0",
            "referer":"https://www.scopus.com/freelookup/form/author.uri?zone=&origin=searchauthorfreelookup",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "origin":"https://www.scopus.com",
            "cookie":'__cfduid=d0ef8c2c5766f13bb1e5f88aede51a58d1551272954; scopus.machineID=41B5E2EE35F904E01336F9C6D10AA5D0.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1551272949963r0.9743103250675618; xmlHttpRequest=true; optimizelyBuckets=%7B%2212850330201%22%3A%2212837340081%22%2C%2210338583043%22%3A%2210332894867%22%7D; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22referral%22%7D; scopusSessionUUID=ea625ad2-5e7f-4135-8; NEW_AE_SESSION_COOKIE=1551595016934; javaScript=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; screenInfo="1080:1920"; NEW_CARS_COOKIE=0069004C00490074006200540068007000620046006F007800710065004600410069002B0059007600750076004F003100720044007700690061006B0036003700650057002F004800500031004D004C006E004D00330066005400470063006A0045006C007800520079006D00730063005400770030004200690051004A006F0059003900410079005000450030003800390068006A004A007600530074005800470052007500500035007A002B002F0068004500340047007500420058006800700034006C005900440037006C00700038007900580034006600570032006C0063002B0065007600730054003600370073007400330077005A004D00700056003200370037006200370042005A004B006A00530059003D; SCSessionID=9CDE83D98B9DA7C17F4E4D3CA4245B31.wsnAw8kcdt7IPYLO0V48gA; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB12BC4EC2FBDE279AD690D20E1B6DCBE7309D569464F19BFE20EC2FAD937301DD8BAFDF2ADE925350150D7900CAD0CA8A6C314CA207F2D090449D5BCEA56104A3B; __cfruid=6d9354eca37678bfa69f0ae6acaf4f08c999987b-1551599927; _pk_ref.2316.d989=%5B%22%22%2C%22%22%2C1551599919%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DBBL2h0wmzA-QTEOPRcPdeBcZUDPr_vjtc7oNk2AoBuNr4RceXzmrIweLz-NA4ahg%26wd%3D%26eqid%3Dc1ea113100047e47000000055c792681%22%5D; _pk_ses.2316.d989=*; _pendo_accountId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A278641; _pendo_visitorId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A37822685; _pendo_meta.7108b796-60e0-44bd-6a6b-7313c4a99c35=2053456852; _pk_id.2316.d989=be0d0f2e50a850bc.1551279111.9.1551600734.1551599919.; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-330454231%7CMCIDTS%7C17959%7CMCMID%7C57604840694696473771710447541746513645%7CMCAAMLH-1552205537%7C11%7CMCAAMB-1552205537%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1551602208s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-164432718%7CvVersion%7C3.1.2; optimizelyPendingLogEvents=%5B%5D; s_pers=%20c19%3Dsc%253Asearch%253Aauthor%2520searchform%7C1551602534989%3B%20v68%3D1551600733606%7C1551602535005%3B%20v8%3D1551600741346%7C1646208741346%3B%20v8_s%3DLess%2520than%25201%2520day%7C1551602541346%3B; s_sess=%20s_cpc%3D0%3B%20c21%3Dlastname%253Djian%2526firstname%253Dli%3B%20e13%3Dlastname%253Djian%2526firstname%253Dli%253A1%3B%20c13%3Ddocument%2520count%2520%2528high-low%2529%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Aauthor%252520searchform%252C77%252C77%252C938%252C1215%252C938%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Aauthor%252520searchform%252C77%252C77%252C938%252C1215%252C938%252C1920%252C1080%252C1%252CP%3B%20s_sq%3Delsevier-sc-prod%25252Celsevier-global-prod%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dsc%2525253Asearch%2525253Aauthor%25252520searchform%252526link%25253D%252525E6%252525A3%25252580%252525E7%252525B4%252525A2%252526region%25253DauthorLookupSearchForm%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%252526pid%25253Dsc%2525253Asearch%2525253Aauthor%25252520searchform%252526pidt%25253D1%252526oid%25253Dfunctiononclick%25252528event%25252529%2525257BcheckAuthOrOrcid%25252528this.form.name%25252529%2525253B%2525257D%252526oidt%25253D2%252526ot%25253DSUBMIT%3B'
        }

    def search_single(self, data):

        first_name = data[0]
        last_name = data[1]
        institute = data[2]
        search_header = self.headers
        search_author_data = {
            "origin": "searchauthorfreelookup",
            "freeSearch": "true",
            "src":"",
            "edit":"",
            "poppUp":"",
            "exactSearch": "on",
            "searchterm1": "jian",
            "searchterm2": "li",
            "institute": "Tsinghua university",
            "submitButtonName": "Search",
            "orcidId":"",
            "authSubject": "LFSC",
            "_authSubject": "on",
            "authSubject": "HLSC",
            "_authSubject": "on",
            "authSubject": "PHSC",
            "_authSubject": "on",
            "authSubject": "SOSC",
            "_authSubject": "on"
        }
        session = requests.Session()
        search_author_data = "origin=searchauthorfreelookup&freeSearch=true&src=&edit=&poppUp=&exactSearch=on&searchterm1=jian&searchterm2=li&institute=Tsinghua+university&submitButtonName=Search&orcidId=&authSubject=LFSC&_authSubject=on&authSubject=HLSC&_authSubject=on&authSubject=PHSC&_authSubject=on&authSubject=SOSC&_authSubject=on"
        search_author_status = 0
        while(search_author_status not in (200,302)):
            try:
                search_author = session.post(self.search_submit, headers = search_header, data=search_author_data)
                search_author_status = search_author.status_code
                search_result = search_author.headers['location']
            except Exception as e:
                print('connect error:%s'%e)
                time.sleep(20)
                print('request try again...')
                search_author_status = 0


        print(search_result)

if __name__ == '__main__':

    scopus_req().search_single(['jian','li','Tsinghua+University'])


