# -*- coding: utf-8 -*-
import sys
sys.path.append('/usr/local/quant/')
from datetime import datetime
import tushare
from data.model import DbHelper, get_all_exchange_abbrev_pkid_dict, get_exchange_by_chinese_ticker
from lib.log import create_logger
import time

logger = create_logger('download_data_by_tushare', '/var/log/quant/download_data_by_tushare.log')

class DownloadStockData(object):
    def __init__(self):
        self.db_helper = DbHelper()
        self.exchange_abbrev_pkid_mapping = get_all_exchange_abbrev_pkid_dict()
        self.exchange_abbrev_pkid_mapping[None] = None

    def init_data_ventor(self):
        return self.db_helper.select_or_insert_one('data_vendor', {'name': 'tushare', 'website_url': 'http://tushare.org'}, ['name'])

    def refresh_symbol(self):
        df = tushare.get_stock_basics()
        insert_rows = []
        self.db_helper.execute('truncate table symbol')
        for t in df.itertuples():
            insert_rows.append({
                'ticker': t[0],
                'name': t[1].replace(' ', '').strip(),
                'sector': t[2],
                'exchange_pkid': self.exchange_abbrev_pkid_mapping[get_exchange_by_chinese_ticker(t[0])],
                'instrument': 'stock',
                'currency': 'RMB'
            })
        self.db_helper.insert_many('symbol', insert_rows)
        logger.info('download symbol count:%s, save db count:%s', len(df), self.db_helper.select_one('select count(1) as c from symbol')['c'])

    def save_one_ticker_daily_price(self, ticker, ktype='D', autype='qfq', start_dt=datetime.now().strftime('%Y-01-01'), end_dt=datetime.now().strftime('%Y-%m-%d')):
        df = tushare.get_k_data(ticker, start=start_dt, end=end_dt, ktype=ktype, autype=autype)
        insert_rows = []
        for d in df.itertuples():
            insert_rows.append({
                'ticker': d[7],
                'price_date': d[1],
                'open_price': float(d[2]),
                'high_price': float(d[4]),
                'close_price': float(d[3]),
                'low_price': float(d[5]),
                'volume': int(d[6]),
                'data_vendor_pkid': 1
            })
        self.db_helper.insert_many('daily_price', insert_rows)
        logger.info('daily_price, ticker:%s, download:%s, save:%s', ticker, len(df), len(insert_rows))

    def download_price_of_all_symbol(self, start_dt=datetime.now().strftime('%Y-01-01'), end_dt=datetime.now().strftime('%Y-%m-%d')):
        symbol_list = self.db_helper.select_all('select ticker from symbol')
        for s in symbol_list:
            try:
                self.save_one_ticker_daily_price(s['ticker'], start_dt=start_dt, end_dt=end_dt)
                self.db_helper.insert_one('download_daily_price_process', {'ticker': s['ticker'], 'st': start_dt, 'et': end_dt, 'result': 1})
            except Exception as e:
                logger.info('download failed ticker:%s,st:%s,dt:%s', s['ticker'], start_dt, end_dt)
                self.db_helper.insert_one('download_daily_price_process', {'ticker': s['ticker'], 'st': start_dt, 'et': end_dt, 'result': 0, 'fail_reason': unicode(e)})


dsd = DownloadStockData()
# dsd.init_data_ventor()
# dsd.refresh_symbol()
# for i in range(2010, 2014, 2):
    # st = time.time()
    # logger.info('start download %s-%s', i, i + 1)
    # dsd.download_price_of_all_symbol(start_dt='%s-01-01' % i, end_dt='%s-12-31' % (i + 1))
    # logger.info('finish download %s-%s', i, i + 1)

dsd.download_price_of_all_symbol(start_dt='2016-01-01', end_dt='2017-04-10')


# dsd.save_one_ticker_daily_price('000858', start_dt='2010-01-01', end_dt='2017-04-10')
# dsd.save_one_ticker_daily_price('002859', start_dt='2010-01-01', end_dt='2017-04-10')
# df = tushare.get_stock_basics()
# print df.ix['002859']['timeToMarket']