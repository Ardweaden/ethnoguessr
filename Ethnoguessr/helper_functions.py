# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:44:57 2018

@author: Jan Jezersek
"""


from wtforms import Form, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('New Password', [
    validators.Required(),
    validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
        
        
    
    