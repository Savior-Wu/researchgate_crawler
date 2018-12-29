#! -*- coding:utf-8 -*-
import pymysql
import time

class db_connection():

    def __init__(self):
        self.db_info = {
            "host":"localhost",
            "account":"researchgate_admin",
            "password":"researchgate",
            "port":3306,
            "default_db":"researchgate"
        }

    def db_connect(self):
        conn = pymysql.connect(
            host = self.db_info['host'],
            port = self.db_info['port'],
            user = self.db_info["account"],
            passwd = self.db_info['password'],
            db = self.db_info["default_db"],
            charset = 'utf8')
        # open then insert success!!
        conn.autocommit(1)
        return conn

    def db_curser(self):
        curser = self.db_connect().cursor()
        return curser

    def db_curser_operater(self):
        conn = self.db_connect()
        curser = self.db_curser()
        return conn, curser

    def db_curser_close(self,conn,curser):
        curser.close()
        conn.close()

    def db_insert_university(self, insert_value, university):
        sql = "insert into %s" %university  + "(per_image, per_profile, per_name, per_university, per_department, per_influence) values " + str(insert_value) + ";"
        conn = self.db_connect()
        curser = self.db_curser()
        try:
            curser.execute(sql)
            conn.commit()
            print('affect rows = {}'.format(curser.rowcount))
        except Exception as e:
            print('Error:%s, **ROLLBACK**' % e)
            conn.rollback()
        curser.close()
        conn.close()

    def db_insert_global(self,insert_value):
        sql = "insert into global_university (continent_name, university_name, stu_number) values" + str(insert_value) + ";"
        conn = self.db_connect()
        curser = self.db_curser()
        try:
            curser.execute(sql)
            conn.commit()
            print('affect rows = {}'.format(curser.rowcount))
        except Exception as e:
            print('Error:%s, **ROLLBACK**' %e )
            conn.rollback()
        curser.close()
        conn.close()

    def read_university(self):
        sql = "select `university_name` from global_university;"
        conn = self.db_connect()
        curser = self.db_curser()
        university_name = []
        try:
            curser.execute(sql)
            print('affect rows = {}'.format(curser.rowcount))
            result = curser.fetchall()
            # like (('Tsinnghua_University',), ('Nanyang_Technological_University',))
            # print(result)
        except Exception as e:
            print('Error:%s, **ROLLBACK**' %e )
            conn.rollback()
        curser.close()
        conn.close()
        for i in result:
            for j in i:
                university_name.append(j)
        return tuple(university_name)

    def create_univer_table(self):
        university = self.read_university()
        # time.sleep(1)
        conn = self.db_connect()
        curser = self.db_curser()
        for i in university:
            univer_table = "oringin_table_" + str(i)
            sql = "create table if not exists %s"\
                  "("\
                "per_id int auto_increment primary key not null,"\
                "per_image text not null,"\
                "per_profile varchar(128) not null,"\
                "per_name varchar(64) not null ,"\
                "per_university varchar(64) not null ,"\
                "per_department text not null ,"\
                "per_influence float not null "\
                ");" %univer_table

            try:
                curser.execute(sql)
                print('affect rows = {}'.format(curser.rowcount))
                conn.commit()
            except Exception as e:
                print('Error:%s, **ROLLBACK**' % e)
                conn.rollback()
        curser.close()
        conn.close()

    def create_univer_person(self):
        university = self.read_university()
        # time.sleep(1)
        conn = self.db_connect()
        curser = self.db_curser()
        for i in university:
            univer_table = "table_" + str(i)
            sql = "create table if not exists %s"\
                  "("\
                "per_id int auto_increment primary key not null,"\
                "per_image text not null,"\
                "per_profile varchar(128) not null,"\
                "per_name varchar(64) not null ,"\
                "per_university varchar(64) not null ,"\
                "per_department text not null ,"\
                "per_influence float not null "\
                ");" %univer_table

            try:
                curser.execute(sql)
                # print('affect rows = {}'.format(curser.rowcount))
                print('create table: table_%s' %univer_table)
                conn.commit()
            except Exception as e:
                print('Error:%s, **ROLLBACK**' % e)
                conn.rollback()
        curser.close()
        conn.close()
        for i in university:
            self.select_from_univer(0,i)
            self.select_from_univer(10, i)
            self.select_from_univer(20, i)
            self.select_from_univer(30, i)

    def insert_into_univer_person(self,target_table, insert_value):
        conn, curser = self.db_curser_operater()
        sql = "insert into table_%s (per_image, per_profile, per_name, per_university, per_department,per_influence) values %s;" %(target_table,str(insert_value))
        try:
            curser.execute(sql)
            conn.commit()
            # print("affect rows = {}".format(curser.rowcount))
        except Exception as e:
            print('Error:%s,**ROLLBACK**' %e)
            conn.rollback()
        self.db_curser_close(conn,curser)

    def select_from_univer(self, tag, target_table):
        conn, curser = self.db_curser_operater()
        if tag == 0:
            sql = "select per_image, per_profile, per_name, per_university, per_department,per_influence from oringin_table_%s where per_id in (" \
                  "select per_id from oringin_table_%s where per_influence>0 and per_influence<=10) order by rand() limit 200;" %(target_table,target_table)
        elif tag == 10:
            sql = "select per_image, per_profile, per_name, per_university, per_department,per_influence from oringin_table_%s where per_id in (" \
                  "select per_id from oringin_table_%s where per_influence>10 and per_influence<=20) order by rand() limit 200;" %(target_table,target_table)
        elif tag == 20:
            sql = "select per_image, per_profile, per_name, per_university, per_department,per_influence from oringin_table_%s where per_id in (" \
                  "select per_id from oringin_table_%s where per_influence>20 and per_influence<=30) order by rand() limit 200;" %(target_table,target_table)
        elif tag == 30:
            sql = "select per_image, per_profile, per_name, per_university, per_department,per_influence from oringin_table_%s where per_id in (" \
                  "select per_id from oringin_table_%s where per_influence>30) order by rand() limit 200;" %(target_table,target_table)
        else:
            print("query table 'oringin_table_%s' error" %target_table)

        try:
            curser.execute(sql)
            data = curser.fetchall()
            print("university:%s  tag:%s" %(target_table, tag))
            print("affect rows = {}".format(curser.rowcount))
            print('********')
        except Exception as e:
            print('Error:%s,**ROLLBACK**' % e)

        self.db_curser_close(conn, curser)

        for i in data:
            self.insert_into_univer_person(target_table, i)

    def db_insert_person_all(self, insert_value):
        conn,curser = self.db_curser_operater()
        sql = "insert into origin_table_person_all(per_image, per_profile, per_name, per_university, per_department,per_influence) values" +str(insert_value) + ";"
        try:
            curser.execute(sql)
            conn.commit()
            print("affect rows = {}".format(curser.rowcount))
        except Exception as e:
            print('Error:%s,**ROLLBACK**' %e)
            conn.rollback()
        self.db_curser_close(conn,curser)

    def db_select_person_univer(self, table_name, number):
        conn,curser = self.db_curser_operater()
        sql = "select per_image, per_profile, per_name, per_university, per_department, per_influence from oringin_table_%s order by per_influence desc limit %s;" %(str(table_name),str(number))
        print(sql)
        try:
            curser.execute(sql)
            print("affect rows = {}".format(curser.rowcount))
            data = curser.fetchall()
            print(data)
        except Exception as e:
            print('Error:%s,**select error**' %e)

        self.db_curser_close(conn,curser)
        for i in data:
            self.db_insert_person_all(i)

    def db_insert_table_person_all(self, insert_value):
        conn,curser = self.db_curser_operater()
        sql = "insert into table_person_all(per_image, per_profile, per_name, per_university, per_department,per_influence) values" +str(insert_value) + ";"
        try:
            curser.execute(sql)
            conn.commit()
            print("affect rows = {}".format(curser.rowcount))
        except Exception as e:
            print('Error:%s,**ROLLBACK**' %e)
            conn.rollback()
        self.db_curser_close(conn,curser)

    def db_select_table_person(self, table_name):
        conn,curser = self.db_curser_operater()
        sql = "select per_image, per_profile, per_name, per_university, per_department, per_influence from table_%s ;" %(str(table_name))
        print(sql)
        try:
            curser.execute(sql)
            print("affect rows = {}".format(curser.rowcount))
            data = curser.fetchall()
            print(data)
        except Exception as e:
            print('Error:%s,**select error**' %e)

        self.db_curser_close(conn,curser)
        for i in data:
            self.db_insert_table_person_all(i)

    # def db_close(self):
    #     # self.conn.cursor().close()
    #     conn.close()

if __name__ == "__main__":
    db_connection().create_univer_person()