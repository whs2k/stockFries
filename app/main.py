# external
from flask import Flask, render_template
import pandas as pd
import json
# internal
from app.config import change_threshold, ownership_colors, positives_colors, negatives_colors

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    with open('json_df.txt', 'r') as f:
        json_df = json.load(f)
    df = pd.read_json(json_df, orient='split')
    ownership = df[['Company', 'Ownership']
                   ].dropna().head(n=20).values.tolist()
    positives = df[(df['Value_x'] > change_threshold) & (df['Value_y'] > change_threshold)].sort_values(
        'Change', ascending=False)[['Company', 'Change']].dropna().head(n=20).values.tolist()
    negatives = df[(df['Value_x'] > change_threshold) & (df['Value_y'] > change_threshold)].sort_values(
        'Change')[['Company', 'Change']].dropna().head(n=20).values.tolist()
    # (possible filter for movement)
    # df[(df['Value_x'] > 100000) & (df['Value_y'] > 100000)]

    return render_template('index.html',
                           ownership=ownership,
                           positives=positives,
                           negatives=negatives,
                           ownership_colors=ownership_colors,
                           positives_colors=positives_colors,
                           negatives_colors=negatives_colors)


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(threaded=True)
