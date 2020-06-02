import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
 

app = Flask(__name__)
#model = pickle.load(open('model2.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('signuploginpage.html')


@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')


@app.route('/loginhandler',methods=['POST','GET'])
def loginhandler():
    features = [str(x) for x in request.form.values()]
    username = features[0]
    password = features[1]

    df = pd.read_csv("storage.csv")

    
    flag=0
    for i in range(len(df)):
        if ( df["Username"][i] == username and df["password"][i]==password ):
            return render_template('index.html', text='Logged In')
            
        else:
            flag = 1
    if(flag==1):
        return render_template('signuploginpage.html', text='Sign Up first')





@app.route('/signup',methods=['POST','GET'])
def signup():
    return render_template('signup.html')


@app.route('/signuphandler',methods=['POST','GET'])
def signuphandler():
    features = [str(x) for x in request.form.values()]
    username = features[0]
    password = features[1]

    df = pd.DataFrame()

    df=pd.read_csv("storage.csv")

    l_username=[]
    l_password=[]

    for i in df["Username"]:
        l_username.append(i)
        
    for i in df["password"]:
        l_password.append(i)

    l_username.append(username)
    l_password.append(password)

    df1 = pd.DataFrame()

    df1["Username"]=l_username
    df1["password"]=l_password

    df1.to_csv("storage.csv")
    return render_template('index.html', text='Succesfully Signed Up!!')


@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]

    total_price = 0
    for i in range(9,26):
        total_price+= int_features[i]

    int_features.append(total_price)
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='The Patient Length of Stay in the Hospital is: {} days'.format(output))



@app.route('/index',methods=['POST'])
def index():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)