from flask import Flask, render_template
import json, requests
app = Flask(__name__)

posts = [
    {
    'author':'Mark Rebetzke',
    'Title':'Blog Post1',
    'content':'First',
    'date':'Today'
    },
    {
    'author':'Mark Rebetzke',
    'Title':'Blog Post2',
    'content':'Second',
    'date':'Today'
    }
]

def get_employee_Data():
    url = "https://reqres.in/api/users"
    headers = {}
    response = requests.get(url=url, headers=headers)
    resp = response.json()
    resp = resp['data']
    return resp

@app.route('/')
def hello_world():
    return 'test'

@app.route('/home')
def blog():
    return render_template('home.html', posts=get_employee_Data(), title='Home')
@app.route('/employees')
def employees():
    return render_template('test.html', employees=get_employee_Data())

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8042)
