from __future__ import print_function
from flask import Flask, render_template, url_for, request, redirect
import sqlite3 as sql
import random

import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'

app=Flask(__name__)
app.secret_key ='shreesathyam'

@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/register')
def register():
    con =sql.connect('inventorymanagement.db')
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute('select *from register')

    users= cur.fetchall()
    con.close()
    return render_template('signup.html')

@app.route('/user/<id>')
def user_info(id):
    with sql.connect('inventorymanagement.db') as con:
        con.row_factory=sql.Row
        cur =con.cursor()
        cur.execute(f'SELECT * FROM register WHERE email="{id}"')
        user = cur.fetchall()
    return render_template("user_info.html", user=user[0])

@app.route('/accessbackend', methods=['POST','GET'])
def accessbackend():
    if request.method == "POST":
        try:
            username=request.form['username']
            email= request.form['email']
            password=request.form['password']

            with sql.connect('inventorymanagement.db') as con:
                cur =con.cursor()
                cur.execute('INSERT INTO register (username ,first_name ,last_name ,mobile, email, password_1 ) VALUES(?,?,?,?,?,?)', (str(username),"shabari","ganesan",9842091510,str(email),str(password)))
                con.commit()
                msg='u r resgistered!'
                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                subject = "Registration Successfull completed!"
                html_content = "<html><body><p>Hey there,\n Your email address has been registered </p></body></html>"
                sender = {"name":"Ganesan shanmugam","email":"ganimoneyyy@gmail.com"}
                to = [{"email":"612419104010cse@gmail.com","name":"Jane Doe"}] 
                cc = [{"email":"shabaripunidha@gmail","name":"Janice Doe"}]
                bcc = [{"name":"John Doe","email":"ganimoneyyy@gmail.com"}]
                reply_to = {"email":"ganimoneyyy@gmail.com","name":"John Doe"}
                headers = {"Some-Custom-Name":"unique-id-1234"}
                params = {"parameter":"My param value","subject":"New Subject"}
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=bcc, cc=cc, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

                try:
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    pprint(api_response)
                except ApiException as e:
                    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    
        except:
            con.rollback()
            msg='some error'      

        finally:
            print(msg)
            return render_template('signup.html')
    else:
        try:
            tue=request.args.get('email')
            tup=request.args.get('password_1')
            print(tue,tup)
            with sql.connect('inventorymanagement.db') as con:
                con.row_factory=sql.Row
                cur=con.cursor()
                cur.execute(f'SELECT password_1 FROM register WHERE email="{tue}"')
                user= cur.fetchall()
        except:
            print('error')
            con.rollback()
        finally:
            if len(user) >0:
                if tup == user[0][0]:
                    return render_template("index.html")
                print(user[0][0])
            return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
