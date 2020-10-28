# external
from flask import Flask, render_template
import pandas as pd
import json
# internal
from config import change_threshold, ownership_colors, positives_colors, negatives_colors

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    """Creates the main page via Flask, reads tables by creating three lists from the json loaded dataframe and loads colors gradients from config"""
    with open('json_df.txt', 'r') as f:
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
                           negatives_colors=negatives_colors)

@app.route("/blog")
def blog():
    return render_template('blog.html')

@app.route("/blog/1_gambling")
def blog1():
    return render_template('BlogPost_1_Gambling.html')

@app.route("/blog/2_basics")
def blog2():
    return render_template('BlogPost_2_Basics.html')

@app.route("/blog/3_covar")
def blog3():
    return render_template('BlogPost_3_Covar.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/sitemap.xml")
def sitemap():
    return render_template('sitemap.xml')


if __name__ == "__main__":
    app.run(threaded=True)
