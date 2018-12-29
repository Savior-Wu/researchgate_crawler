#! -*- coding:utf-8 -*-

import json
from core.db_connect import db_connection

class read_file():
    def __init__(self):
        self.file_loc = '../source_data/university_json'

    def deal_data(self):
        global_data = []

        with open(self.file_loc, 'r') as f:
            origin_data = json.load(f)

        for key, value in origin_data.items():
            for i in value:
                for del_key, del_value in i.items():
                    global_data.append([key,del_key,del_value])
        return global_data

    def data_to_db(self):
        data = self.deal_data()
        for i in data:
            db_connection().db_insert_global(tuple(i))

    def university_number_to_db(self):
        data = self.deal_data()
        for i in data:
            db_connection().db_select_person_univer(i[1],i[2])

    def table_all(self):
        data = self.deal_data()
        for i in data:
            db_connection().db_select_table_person(i[1])

if __name__ == '__main__':
    read_file().table_all()
