from flask import *  
from script import runScript
app = Flask(__name__)  
  
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user', methods = ['POST'])  
def login():  
      keyWord=request.form['uname']
      ans = runScript(keyWord)
      return '<div>' +ans+ '</div>' 

if __name__ == '__main__':  
   app.run(debug = True)  