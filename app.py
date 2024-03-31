from flask import Flask, render_template, flash, redirect, url_for, session, request
import pandas as pd
from sqlalchemy import create_engine
from dateutil.parser import parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key' 

# MySQL connection details (replace with your credentials)
db_engine = create_engine('mysql://<username>:<password>@<hostname>/<database_name>')

@app.route("/", methods=["GET", "POST"])
def data_upload_page():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file: 
            df = pd.read_csv(uploaded_file, dtype=object)
            df['Date'] = pd.to_datetime(df['Date'])
            # ... (Column cleaning if needed)
            try: 
               df.to_sql('table_name', con=db_engine, if_exists='replace')
               flash('Data uploaded successfully!') 
               return redirect(url_for("grafanadashboard"))
            except Exception as e:
               flash(f'An error occurred during upload: {e}') 

        else:
            flash('No file selected.')
    return render_template('index.html') 

@app.route("/grafanadashboard")
def grafanadashboard():
    return render_template('grafana_dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
