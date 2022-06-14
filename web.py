from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/follower', methods=['GET', 'POST'])
def follower():
    data = pd.read_csv('follower.csv')
    return render_template('simple.html', tables=[data.to_html()], titles=[''])

@app.route('/repos', methods=['GET','POST'])
def repos():
    data = pd.read_csv('repos.csv')
    return render_template('simple.html', tables=[data.to_html()], titles=[''])

@app.route('/user', methods=['GET', 'POST'])
def userRepo():
    data = pd.read_csv('reposito.csv')
    return render_template('simple.html', tables=[data.to_html()], titles=[''])

if __name__ == "__main__":
    app.run()