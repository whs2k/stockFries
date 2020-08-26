# external
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
# internal
from app.config import fund_dict


def forms_scraper(fund_link):
    r = requests.get(fund_link)
    soup = BeautifulSoup(r.content, 'html.parser')
    filing_links = []
    table = soup.find_all('table')[2]
    rows = [i for i in table.find_all('tr')]
    for i in rows:
        cols = i.find('td')
        if cols is not None:
            if '13F-HR' in cols.text:
                base_link = 'https://www.sec.gov'
                link = i.find('a').get('href')
                filing_links.append(base_link + link)

    form_links = []
    for i in filing_links[:2]:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        rows = [i for i in table.find_all('tr')]
        form_links.append(base_link + rows[3].find('a').get('href'))
    return form_links


def shares_scraper(form_link):
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
            shares_list.append({'CUSIP': i[2][:6], 'Company': i[0], 'Value': int(i[3].replace(',', '')),
                                'Shares': int(i[4].replace(',', ''))})

    return shares_list


def pandas_analysis(fund_dict):
    list_current = []
    list_previous = []
    for k, v in fund_dict.items():
        try:
            forms = forms_scraper(v)
            print(forms)
            shares_list_current = shares_scraper(forms[0])
            list_current.extend(shares_list_current)
            shares_list_previous = shares_scraper(forms[1])
            list_previous.extend(shares_list_previous)
        except:
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
    with open('json_df.txt', 'w') as f:
        json.dump(json_df, f)


if __name__ == "__main__":
    pandas_analysis(fund_dict)
