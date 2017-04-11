# -*- coding: utf-8 -*-
import pymysql

DATABASE_SETTING = {
    'host': '127.0.0.1',
    'user': 'quant',
    'password': 'quant',
    'db': 'quant',
    'port': 3306,
    'charset': 'utf8'
}

EXCHANGE_SZ_A = 'SZ-A'
EXCHANGE_SZ_B = 'SZ-B'
EXCHANGE_SH_A = 'SH-A'
EXCHANGE_SH_B = 'SH-B'
EXCHANGE_SME = 'SME'
EXCHANGE_GME = 'GME'

def get_exchange_by_abbrev(abbrev):
    return DbHelper().select_one('select * from exchange where abbrev=%s', tuple([abbrev]))

def get_all_exchange_abbrev_pkid_dict():
    rows = DbHelper().select_all('select pkid,abbrev from exchange')
    d = {}
    for i in rows:
        d[i['abbrev']] = i['pkid']
    return d

def get_exchange_by_chinese_ticker(ticker):
    ticker = str(ticker)
    if ticker.startswith('601') or ticker.startswith('600') or ticker.startswith('603'):
        return EXCHANGE_SH_A
    elif ticker.startswith('900'):
        return EXCHANGE_SH_B
    elif ticker.startswith('000'):
        return EXCHANGE_SZ_A
    elif ticker.startswith('200'):
        return EXCHANGE_SZ_B
    elif ticker.startswith('002'):
        return EXCHANGE_SME
    elif ticker.startswith('300'):
        return EXCHANGE_GME
    else:
        return None

class DbHelper(object):
    def __init__(self, database_setting=None):
        self.database_setting = database_setting or DATABASE_SETTING

    def get_conn(self):
        return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **self.database_setting)

    def execute(self, sql, val_tuple=None, get_lastrowid=False):
        conn = self.get_conn()
        try:
            cur = conn.cursor()
            cur.execute(sql, val_tuple)
            cur.close()
            conn.commit()
            if get_lastrowid:
                return cur.lastrowid
            else:
                return cur.rowcount
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    def executemany(self, sql, val_list):
        conn = self.get_conn()
        try:
            cur = conn.cursor()
            cur.executemany(sql, val_list)
            cur.close()
            conn.commit()
            return cur.rowcount
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    def select_one(self, sql, val_tuple=None):
        conn = self.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, val_tuple)
                return cur.fetchone()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    def select_all(self, sql, val_tuple=None):
        conn = self.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, val_tuple)
                return cur.fetchall()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    def insert_one(self, table_name, row_dict):
        field_list = '`' + '`,`'.join(row_dict.keys()) + '`'
        val_list = ','.join(len(row_dict) * ['%s'])

        insert_sql = 'INSERT INTO `{table_name}`({field_list}) VALUES({val_list})'.format(
            table_name=table_name,
            field_list=field_list,
            val_list=val_list
        )
        return self.execute(insert_sql, tuple(row_dict.values()), get_lastrowid=True)

    def insert_many(self, table_name, row_dict_list):
        field_list = '`' + '`,`'.join(row_dict_list[0].keys()) + '`'
        val_list = ','.join(len(row_dict_list[0]) * ['%s'])

        insert_sql = 'INSERT INTO `{table_name}`({field_list}) VALUES({val_list})'.format(
            table_name=table_name,
            field_list=field_list,
            val_list=val_list
        )
        return self.executemany(insert_sql, [d.values() for d in row_dict_list])

    def _where(self, row_dict):
        field_list, val_list = [], []
        for k, v in row_dict.items():
            if v is None:
                field_str = '`{0}` is NULL'.format(k)
            else:
                field_str = '`{0}`=%s'.format(k)
                val_list.append(v)
            field_list.append(field_str)
        return 'WHERE ' + ' and '.join(field_list) if len(field_list) > 0 else '', val_list

    def select_or_insert_one(self, table_name, row_dict, unique_key_list):
        where_str, where_val_list = self._where({uk: row_dict[uk] for uk in unique_key_list})
        select_sql = 'SELECT pkid FROM {table_name} {where_str}'.format(table_name=table_name, where_str=where_str)
        exist_row = self.select_one(select_sql, tuple(where_val_list))
        if exist_row:
            return exist_row['pkid']
        else:
            return self.insert_one(table_name, row_dict)


