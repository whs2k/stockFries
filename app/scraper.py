# external
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
# internal
import config
#from config import fund_dict, scrapped_json_fn_no_ticker, scrapped_json_fn, openfigi_apikey
import os
import re
import datetime


def forms_scraper(fund_link):
    """Takes the SEC fund link to return the 2 most recent filing URLS"""
    r = requests.get(fund_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    filing_links = []
    filing_dates = []
    table = soup.find_all('table')[2]
    rows = [i for i in table.find_all('tr')]
    for i in rows:
        cols = i.find('td')
        if cols is not None:
            if '13F-HR' in cols.text:
                base_link = 'https://www.sec.gov'
                link = i.find('a').get('href')
                filing_links.append(base_link + link)
                date = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})\n",(i.text)).group()
                #print('date:::::', date)
                filing_dates.append(date)
    max_filing_date = str(max(filing_dates)).replace('\n','')

    form_links = []
    for i in filing_links[:2]:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        rows = [i for i in table.find_all('tr')]
        form_links.append(base_link + rows[3].find('a').get('href'))
    return form_links, max_filing_date


def shares_scraper(form_link):
    """Takes a filing link and appends all holdings to a list"""
    r = requests.get(form_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all('table')[3]
    rows = table.find_all('tr')[3:]

    shares_list = []
    rows_text = []
    for i in rows:
        cols = i.find_all('td')
        cols_text = []
        for col in cols:
            if col is not None:
                cols_text.append(col.text)
        rows_text.append(cols_text)

    for i in rows_text:
        if (i[6] != 'Put') or (i[6] != 'Call'):
            shares_list.append({'CUSIP': i[2][:9], 'Company': i[0], 'Value': int(i[3].replace(',', '')),
                                'Shares': int(i[4].replace(',', ''))})

    return shares_list


def pandas_analysis(fund_dict):
    """Takes the fund dict and gets the filings URLS from forms_scraper, then extends two aggregate lists for the current and previous holdings across all funds before analysis in pandas and export to json txt"""
    list_current = []
    list_previous = []
    fund_dict_scraped_current = {}
    fund_dict_scraped_previous = {}
    for fund_name, fund_link in fund_dict.items():
        try:
            forms, max_form_date = forms_scraper(fund_link)
            print(datetime.datetime.now(), ' :: Scrpaing :: ',forms)
            shares_list_current = shares_scraper(forms[0])
            list_current.extend(shares_list_current)
            shares_list_previous = shares_scraper(forms[1])
            list_previous.extend(shares_list_previous)
            fund_dict_scraped_current[fund_name] = [fund_link, max_form_date, shares_list_current,shares_list_current]
            fund_dict_scraped_previous[fund_name] = [fund_link, max_form_date, shares_list_current,shares_list_previous]
        except Exception as e:
            print('We got an error here!:', e, flush=True)
            pass

    df_current = pd.DataFrame(list_current)
    dfc = df_current.groupby('CUSIP').agg(
        {'Company': 'first', 'Value': 'sum', 'Shares': 'sum'})
    dfc['Company'] = dfc['Company'].str.title()
    dfc['Ownership'] = (dfc['Value'] / dfc['Value'].sum()) * 100
    dfc = dfc.sort_values('Ownership', ascending=False).round(2)

    df_previous = pd.DataFrame(list_previous)
    dfp = df_previous.groupby('CUSIP').agg(
        {'Company': 'first', 'Value': 'sum', 'Shares': 'sum'})
    dfp['Company'] = dfp['Company'].str.title()

    dff = pd.merge(dfc, dfp, on=['CUSIP', 'Company'], how='outer')
    dff['Change'] = ((dff['Shares_x'] - dff['Shares_y']) /
                     dff['Shares_x']) * 100

    json_df = dff.round(2).to_json(orient='split')
    with open(config.scrapped_json_fn_no_ticker, 'w') as f:
        json.dump(json_df, f)

    json_df_byfund = pd.DataFrame(fund_dict_scraped_current).to_json(orient='split')
    with open(config.scrapped_json_fn_hedgefund, 'w') as f:
        json.dump(json_df_byfund, f)
    #print(df_byfund.tail(), flush=True)

def get_tickers_from_cusips(list_of_cusips_):
    '''
    input: list_of_cusips
    output: list_of_stock_tickers
    '''
    #jobs_ = [{'idType':'ID_CUSIP','idValue':cusip} for cusip in list_of_cusips_]
    list_of_tickers = []
    openfigi_apikey = config.figi_api_key 
    openfigi_url = 'https://api.openfigi.com/v2/mapping'
    openfigi_headers = {'Content-Type': 'text/json'}
    if openfigi_apikey:
        openfigi_headers['X-OPENFIGI-APIKEY'] = openfigi_apikey
    for cusip in list_of_cusips_:
        job_ = [{'idType':'ID_CUSIP','idValue':cusip}]
        try:
            response = requests.post(url=openfigi_url, headers=openfigi_headers,
                         json=job_)
            respon_json = response.json()
            response_ticker = respon_json[0]['data'][0]['ticker']
            list_of_tickers.append(response_ticker)
            #print(response_ticker)
        except:
            list_of_tickers.append(None)
    return list_of_tickers

def generate_yahoo_link(ticker_):
    return 'https://finance.yahoo.com/quote/{}?p={}'.format(str(ticker_),str(ticker_))

def generate_and_save_tiker_yahoo_json(fn_):
    '''
    input: fn; absolute paht
    output: json df with stocker ticker and 
        yahoo url colums added and re-saved
    '''
    with open(fn_, 'r') as f:
        json_df = json.load(f)
    df_ = pd.read_json(json_df, orient='split').rename_axis('cusip').reset_index()#
    list_of_cusips = df_.cusip.tolist()
    df_['ticker'] = get_tickers_from_cusips(list_of_cusips)
    df_['URL_Yahoo'] = df_.ticker.apply(generate_yahoo_link)
    json_df_ = df_.to_json(orient='split')
    with open(fn_, 'w') as f:
        json.dump(json_df_, f)
    



if __name__ == "__main__":
    pandas_analysis(config.fund_dict)
    generate_and_save_tiker_yahoo_json(config.scrapped_json_fn_no_ticker)
