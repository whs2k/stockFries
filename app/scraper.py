# built-in
import os
import re
import datetime
import shutil
import traceback
from typing import Tuple
# external
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
# internal
import config
from emailer import EmailBase


def forms_scraper(fund_link: str) -> Tuple[list, str]:
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
                date = re.search(
                    "([0-9]{4}\-[0-9]{2}\-[0-9]{2})\n", (i.text)).group()
                #print('date:::::', date)
                filing_dates.append(date)
    max_filing_date = str(max(filing_dates)).replace('\n', '')

    form_links = []
    for i in filing_links[:2]:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        rows = [i for i in table.find_all('tr')]
        form_links.append(base_link + rows[3].find('a').get('href'))
    return form_links, max_filing_date


def shares_scraper(form_link: str, name_of_hf: str) -> Tuple[list, list]:
    """Takes a filing link and appends all holdings to a list"""
    r = requests.get(form_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all('table')[3]
    rows = table.find_all('tr')[3:]

    shares_list = []
    options_list = []
    rows_text = []
    for i in rows:
        cols = i.find_all('td')
        cols_text = []
        for col in cols:
            if col is not None:
                cols_text.append(col.text)
        rows_text.append(cols_text)
    #print('rows_text: ', rows_text, flush=True)

    for i in rows_text:
        #print('i: ', i, flush=True)
        if (i[6] != 'Put') or (i[6] != 'Call'):
            shares_list.append({'CUSIP': i[2][:9], 'Company': i[0], 'Value': int(i[3].replace(',', '')),
                                'Shares': int(i[4].replace(',', ''))})
        if (i[6] == 'Put') or (i[6] == 'Call'):
            #print('i: ',i)
            options_list.append({'HF_Name': name_of_hf, 'CUSIP': i[2][:9], 'Company': i[0], 'Value':
                                 int(i[3].replace(',', '')),
                                 'Shares': int(i[4].replace(',', '')), 'Option_Type': i[6]})

    return shares_list, options_list


def pandas_analysis(fund_dict: dict) -> None:
    """Takes the fund dict and gets the filings URLS from forms_scraper, then extends two aggregate lists for the
    current and previous holdings across all funds before analysis in pandas and export to json txt """

    list_current = []
    list_previous = []
    fund_dict_scraped_current = {}
    fund_dict_scraped_previous = {}
    options_list_current_full = []
    options_list_previous_full = []
    for fund_name, fund_link in fund_dict.items():
        try:
            forms, max_form_date = forms_scraper(fund_link)
            print(datetime.datetime.now(), ' :: Scrpaing :: ', forms)
            shares_list_current, options_list_current = shares_scraper(forms[0],
                                                                       name_of_hf=fund_name)
            list_current.extend(shares_list_current)
            options_list_current_full.extend(options_list_current)
            shares_list_previous, options_list_previous = shares_scraper(forms[1],
                                                                         name_of_hf=fund_name)
            list_previous.extend(shares_list_previous)
            options_list_previous_full.extend(options_list_previous)
            fund_dict_scraped_current[fund_name] = [
                fund_link, max_form_date, shares_list_current, shares_list_current]
            fund_dict_scraped_previous[fund_name] = [
                fund_link, max_form_date, shares_list_current, shares_list_previous]
            #print('options_list_current_full: ',options_list_current_full, flush=True)
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

    json_df = dff.round(2).reset_index().to_json(orient='split')
    print('json_df: ', dff.head(), flush=True)  # previoulsy dffxfno_.head()
    with open(config.scrapped_json_fn_no_ticker, 'w') as f:
        print('saving to: ', config.scrapped_json_fn_no_ticker)
        print()
        json.dump(json_df, f)

    json_df_byfund = pd.DataFrame(
        fund_dict_scraped_current).to_json(orient='split')
    with open(config.scrapped_json_fn_hedgefund, 'w') as f:
        json.dump(json_df_byfund, f)

    df_options = pd.DataFrame(options_list_current_full)
    json_df_options = df_options.to_json(orient='split')
    print('json_df_options: ', df_options.head(), flush=True)
    with open(config.scrapped_json_fn_options, 'w') as f:
        print('saving to: ', config.scrapped_json_fn_options)
        json.dump(json_df_options, f)

    try:  # Copy over files to static folder for downloading
        to_static_fn_byHF = os.path.join(os.getcwd(),
                                         'static', os.path.basename(config.scrapped_json_fn_hedgefund))
        print('Copying File to: ', to_static_fn_byHF, flush=True)
        shutil.copyfile(config.scrapped_json_fn_hedgefund, to_static_fn_byHF)

        to_static_fn_options = os.path.join(os.getcwd(),
                                            'static', os.path.basename(config.scrapped_json_fn_options))
        print('Copying File to: ', to_static_fn_options, flush=True)
        shutil.copyfile(config.scrapped_json_fn_options, to_static_fn_options)
    except Exception as e:
        print('Error in file Copy: ', e, flush=True)
    #print(df_byfund.tail(), flush=True)


def get_tickers_from_cusips(list_of_cusips_: list) -> list:
    """
    input: list_of_cusips
    output: list_of_stock_tickers
    """

    #jobs_ = [{'idType':'ID_CUSIP','idValue':cusip} for cusip in list_of_cusips_]
    list_of_tickers = []
    openfigi_apikey = config.figi_api_key
    openfigi_url = 'https://api.openfigi.com/v2/mapping'
    openfigi_headers = {'Content-Type': 'text/json'}
    if openfigi_apikey:
        openfigi_headers['X-OPENFIGI-APIKEY'] = openfigi_apikey
    for cusip in list_of_cusips_:
        job_ = [{'idType': 'ID_CUSIP', 'idValue': cusip}]
        try:
            response = requests.post(url=openfigi_url, headers=openfigi_headers,
                                     json=job_)
            respon_json = response.json()
            response_ticker = respon_json[0]['data'][0]['ticker']
            list_of_tickers.append(response_ticker)
            #print('Sucessful response_ticker: ',response_ticker,flush=True)
        except Exception as exc:
            list_of_tickers.append(None)
            print('Error in get_tickers_from_cusips; CUSIP:  ', cusip, flush=True)
            print('JSON_Response: ', respon_json, flush=True)
            print(traceback.format_exc(), flush=True)
        #print('list_of_tickers: ', list_of_tickers, flush=True)
    return list_of_tickers


def generate_yahoo_link(ticker_: str) -> str:
    return 'https://finance.yahoo.com/quote/{}?p={}'.format(str(ticker_), str(ticker_))


def generate_and_save_ticker_yahoo_json(input_fn_, export_fn_) -> None:
    """
    input: fn; absolute path
    output: json df with stock ticker and
        yahoo url columns added and re-saved
    """
    with open(input_fn_, 'r') as f:
        json_df = json.load(f)
    # .rename_axis('cusip').reset_index()#
    df_ = pd.read_json(json_df, orient='split')
    print('loaded in generate_and_save_tiker_yahoo_json: ', df_.tail())
    list_of_cusips = df_.cusip.tolist()
    df_['ticker'] = get_tickers_from_cusips(list_of_cusips)
    df_['URL_Yahoo'] = df_.ticker.apply(generate_yahoo_link)
    json_df_ = df_.to_json(orient='split')
    # with open(input_fn_, 'w') as f:
    #    json.dump(json_df_, f)
    with open(export_fn_, 'w') as f:
        json.dump(json_df_, f)
        print('Saving File to: ', export_fn_, flush=True)
    try:  # Copy over files to static folder for downloading
        to_static_fn_input = os.path.join(os.getcwd(),
                                          'static', os.path.basename(input_fn_))
        to_static_fn_export = os.path.join(os.getcwd(),
                                           'static', os.path.basename(export_fn_))
        print('Copying File to: ', to_static_fn_input, flush=True)
        shutil.copyfile(input_fn_, to_static_fn_input)
        print('Copying File to: ', to_static_fn_export, flush=True)
        shutil.copyfile(export_fn_, to_static_fn_export)
    except Exception as e:
        print('Error in file Copy: ', e, flush=True)


if __name__ == "__main__":
    try:
        pandas_analysis(config.fund_dict)
        generate_and_save_ticker_yahoo_json(
            config.scrapped_json_fn, config.scrapped_json_fn)
        EmailBase().email_template('Scraper succeeded')
    except Exception as e:
        EmailBase().email_template(f'Scraper failed with error {e}')

