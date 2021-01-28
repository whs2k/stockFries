# external
from flask import Flask, render_template
import pandas as pd
import json
# internal
import config
from config import change_threshold, ownership_colors, positives_colors, negatives_colors

pd.set_option('display.max_colwidth', -1)
app = Flask(__name__)

#fn_dataByHedge = 'json_df_dataByHedgeFund.txt'
#fn2 = 'json_df_no_ticker.txt'
#fn = os.path.join(os.path.dirname(os.getcwd()), 'app', 'json_df.txt') #app/json_df.txt

with open(config.scrapped_json_fn_hedgefund, 'r') as f:
    hedge_fund_json_dg = json.load(f)
df_recent_filing = pd.read_json(hedge_fund_json_dg, orient='split').T.rename(columns={0:'link',1:'recent_filing_date',2:'current_holdings',3:'previous_holdings'})
df_recent_filing_head = df_recent_filing [df_recent_filing.recent_filing_date == df_recent_filing.recent_filing_date.max()].head(1)
most_recent_filing_date = df_recent_filing_head.recent_filing_date.tolist()[0]
most_recent_filing_url = df_recent_filing_head.link.tolist()[0]
most_recent_filing_fund = df_recent_filing_head.index.tolist()[0]

@app.route("/", methods=['GET', 'POST'])
def index():
    """Creates the main page via Flask, reads tables by creating three lists from the json loaded dataframe and loads colors gradients from config"""
    with open(config.scrapped_json_fn, 'r') as f:
        json_df = json.load(f)
    df = pd.read_json(json_df, orient='split')
    try:
        ownership = df[['Company', 'Ownership','URL_Yahoo']
                     ].dropna().head(n=20).values.tolist()
    except:
      ownership = df[['Company', 'Ownership']
                     ].dropna().head(n=20).values.tolist()
    positives = df.sort_values(
        'Change', ascending=False)[['Company', 'Change','URL_Yahoo']].dropna().head(n=20).values.tolist()
    negatives = df.sort_values(
        'Change')[['Company', 'Change','URL_Yahoo']].dropna().head(n=20).values.tolist()

    return render_template('index.html',
                           ownership=ownership,
                           positives=positives,
                           negatives=negatives,
                           ownership_colors=ownership_colors,
                           positives_colors=positives_colors,
                           negatives_colors=negatives_colors,
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)

@app.route("/data_byHedgeFund", methods=['GET', 'POST'])
def index_byHedgeFund():
    """Creates the main page via Flask, reads tables by creating three lists from the json loaded dataframe and loads colors gradients from config"""
    try:
      filings_by_fund = df_recent_filing.reset_index().rename(columns={'index':'fund_name'}) \
                    [['fund_name','recent_filing_date','current_holdings','previous_holdings','link']
                    ].dropna().head(n=50).values.tolist()
      for i, fund_filing in enumerate(filings_by_fund):
        filings_by_fund_stocksOnly = [x['Company'] for x in fund_filing[2]]
        filings_by_fund[i].insert(6, filings_by_fund_stocksOnly)
      #print(filings_by_fund[0][5])
    except Exception as e:
      print('Error Pulling outt Filings by Fund', flush=True)
      print(e, flush=True)
      pass
    return render_template('index_byHedgeFund.html',
                          filings_by_fund=filings_by_fund,
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)

@app.route("/shorts", methods=['GET', 'POST'])
def index_shorts():
    """Lists Options"""
    #try:
    with open(config.scrapped_json_fn_options, 'r') as f:
        hedge_fund_json_dg = json.load(f)
    df_recent_options = pd.read_json(hedge_fund_json_dg, orient='split')
    df_puts_only = df_recent_options.drop_duplicates(subset=['CUSIP','HF_Name'], keep=False)
    df_puts_only = df_puts_only[(df_puts_only['Option_Type']=='Put') & (df_puts_only['HF_Name']!='CAPITAL FUND MANAGEMENT')]
    #df_puts_only.sort_values('Company').reset_index().tail(100)
    df_puts_only_by_stock = df_puts_only.groupby(['CUSIP','Company','Option_Type'],as_index=False).agg(
        {'Shares': 'sum', 'Value': 'sum', 'HF_Name': 'unique'}).sort_values('Value',ascending=False)
    puts_only_by_stock = df_puts_only_by_stock[['Company', 'Option_Type','Shares','Value','HF_Name']
                     ].dropna().head(n=75).values.tolist()
    #except Exception as e:
      #print('Error Pulling outt Options by Stock', flush=True)
      #print(e, flush=True)
      #pass
    return render_template('index_options_byStock.html',
                          put_options_by_stock=puts_only_by_stock,
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)

@app.route("/blog")
def blog():
    return render_template('blog.html',
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)

@app.route("/blog/1_gambling")
def blog1():
    return render_template('BlogPost_1_Gambling.html',
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)

@app.route("/blog/2_basics")
def blog2():
    return render_template('BlogPost_2_Basics.html',
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)

@app.route("/blog/3_covar")
def blog3():
    return render_template('BlogPost_3_Covar.html',
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)
@app.route("/blog/4_strats")
def blog4():
    return render_template('BlogPost_4_Strats.html',
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)

@app.route("/about")
def about():
    fund_link_dictionary_list = [[key, val] for key, val in config.fund_dict.items()]
    return render_template('about.html',
                          fund_name_link_zipped_list=fund_link_dictionary_list,
                           most_recent_filing_url=most_recent_filing_url,
                           most_recent_filing_firm=most_recent_filing_fund,
                           most_recent_filing_date=most_recent_filing_date)

@app.route("/sitemap.xml")
def sitemap():
    return render_template('sitemap.xml')

@app.route("/ads.txt")
def ads_txt():
    return render_template('ads.txt')


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
