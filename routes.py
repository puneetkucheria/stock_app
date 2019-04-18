from flask import Flask, render_template, request, jsonify
from dbfun import get,data_status
from bhavweb import updatebhavedata, add_dates
''' Update bhav data in database'''

app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/')
def home():
  return jsonify(get())

@app.route('/data_status')
def data_status1():
  return jsonify(data_status())

@app.route('/updatebhavedata')
def updatebhavedata1():
  return jsonify(updatebhavedata())

@app.route('/adddates')
def adddates():
  return jsonify(add_dates(50))

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5002)
