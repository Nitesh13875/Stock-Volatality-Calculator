from flask import Flask, render_template, request
import os
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def calculate_metrics(csv_path):
    try:
        # Try reading with UTF-8 encoding
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            # Try reading with ISO-8859-1 encoding
            df = pd.read_csv(csv_path, encoding='ISO-8859-1')
        except UnicodeDecodeError:
            return None, None, None

    # Calculate Daily Returns
    df['Return'] = df['Close'].pct_change()
    df.at[0, 'Daily Returns'] = 0

    # Calculate Daily Volatility
    daily_volatility = df['Return'].std()

    # Calculate Annualized Volatility
    data_length = len(df)
    annualized_volatility = daily_volatility * np.sqrt(data_length)

    return df, daily_volatility, annualized_volatility

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', message='No selected file')

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        df, daily_volatility, annualized_volatility = calculate_metrics(file_path)

        if df is None or daily_volatility is None or annualized_volatility is None:
            return render_template('index.html', message='Error decoding the file. Please check the file encoding.')

    
        return render_template('index.html',daily_volatility=daily_volatility,
                               annualized_volatility=annualized_volatility)

if __name__ == '__main__':
    app.run(debug=True)
