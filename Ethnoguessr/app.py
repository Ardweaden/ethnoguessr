# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:55:55 2018

@author: Jan Jezersek
"""

from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, session
import requests
import json
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from helper_functions import RegistrationForm
import random
import numpy as np

app = Flask(__name__)
app.secret_key = '314159265358979323846'

@app.route('/', methods=['POST','GET'])
def index_page():
    session['logged_in'] = False
    return render_template('index.html')


@app.route('/login',methods = ['POST','GET'])
def login_page():
    try:
        if request.method == 'POST':
            not_found = 1
            
            entered_password = request.form['password']
            entered_username = request.form['username']
            
            with open("C:/Users/Jan Jezersek/Documents/Python Scripts/Ethnoguessr/users.txt","r") as f:
                data = f.readlines()
                        
            for i in range(0,len(data),2):
                if data[i][:-1] == entered_username:
                    real_password = data[i+1][:-1]
                    not_found = 0
            
            if not_found:
                print("Wrong password, try again")
                return render_template('login.html')
            
            if entered_password == real_password:
                session['logged_in'] = True
                session['username'] = entered_username
                return redirect('/play')
            else:
                print('Wrong password. Please try again.')
                return render_template('login.html')
        else:
            return render_template('login.html')
    except:
        return render_template('login.html')
    

@app.route('/register',methods = ['POST','GET'])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            password = form.password.data            

            with open("C:/Users/Jan Jezersek/Documents/Python Scripts/Ethnoguessr/users.txt","r") as f:
                users = f.readlines()
            
            for i in range(0,len(users),2):
                if users[i][:-1] == username:
                    flash("That username is already taken, please choose another")
                    return render_template('register.html', form=form)

            else:
                session['logged_in'] = False
                session['username'] = username
                
                with open("C:/Users/Jan Jezersek/Documents/Python Scripts/Ethnoguessr/users.txt","a") as f:
                    f.write(username + "\n")
                    f.write(password + "\n")
                    
                with open("C:/Users/Jan Jezersek/Documents/Python Scripts/Ethnoguessr/leaderboard.txt","a") as f:
                    f.write(username + "\n")
                    f.write("0\n")
                    f.write("0\n")
                    f.write("0\n")
                
                return redirect(url_for('login_page'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
        
@app.route('/play',methods = ['POST','GET'])
def play_page():
    
    if request.method == 'GET':
        if session['logged_in']:
            return render_template("ethnoguessr.html")
        else:
            return redirect(url_for('login_page'))
    
@app.route('/choose_image')
def choose_image():
        if request.method == 'GET':
            with open("C:/Users/Jan Jezersek/Documents/Python Scripts/Ethnoguessr/pictures.txt","r") as f:
                data = f.readlines()
                
            i = 2*(int(random.random()*len(data)/2))
            url = data[i][:-1]
            coordinates = data[i+1][:-1]
            return jsonify(url,coordinates)
        
@app.route('/save_results',methods = ['POST'])
def save_results():
    result = request.form['score']
    
    with open("C:/Users/Jan Jezersek/Documents/Python Scripts/Ethnoguessr/leaderboard.txt","r") as f:
        leaderboard = f.readlines()
    
    for i in range(0,len(leaderboard),4):
        if leaderboard[i][:-1] == session['username']:
            score = int(leaderboard[i+1][:-1]) + int(result)
            n_games = int(leaderboard[i+2][:-1]) + 1
            print(score,n_games,type(score),type(n_games))
            leaderboard[i+3] = str(float(float(score)/n_games)) + '\n'
            leaderboard[i+1] = str(score) + '\n'
            leaderboard[i+2] = str(n_games) + '\n'     
    
    with open("C:/Users/Jan Jezersek/Documents/Python Scripts/Ethnoguessr/leaderboard.txt","w") as f:
        f.writelines(leaderboard)
        
    return jsonify("kek")

@app.route('/leaderboard',methods = ['GET'])
def leaderboard_page():
    cumulative_leaders, usernames, average_leaders = [],[],[]

    with open("C:/Users/Jan Jezersek/Documents/Python Scripts/Ethnoguessr/leaderboard.txt","r") as f:
        leaderboard = f.readlines()
        
    for i in range(1,len(leaderboard),4):
        cumulative_leaders.append(int(leaderboard[i][:-1]))
        average_leaders.append(float(leaderboard[i+2][:-1]))
        usernames.append(leaderboard[i-1][:-1])
        
    cumulative_leaders = np.array(cumulative_leaders)
    average_leaders = np.array(average_leaders)
    usernames = np.array(usernames)
    cumulative_indices = np.argsort(-cumulative_leaders)
    average_indices = np.argsort(-average_leaders)
    
    cumulative_usernames = usernames[cumulative_indices]
    cumulative_leaders = cumulative_leaders[cumulative_indices]
    
    average_usernames = usernames[average_indices]
    average_leaders = average_leaders[average_indices]
        
    cl = []
    al = []
    
    for i in range(len(cumulative_leaders)):
        cl.append([cumulative_usernames[i],cumulative_leaders[i]])
        al.append([average_usernames[i],average_leaders[i]])
    
    return render_template("leaderboard.html",cl=cl,al=al)         

app.run(debug=True,threaded=True)