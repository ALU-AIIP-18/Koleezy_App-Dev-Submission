import flask
import dashboard
import flask
import sms_content
from twilio import twiml
from twilio.rest import TwilioRestClient

from flask import render_template
import os
from twilio.rest import Client



account_sid = 'ACa6910ef9f48d06115bd60e7e06418417' #Enter your credentials
auth_token = '18991608ce67b93c1946b9aac6e69302'    #Enter your account token
client = Client(account_sid, auth_token)


server = flask.Flask(__name__)

import dash_html_components as html
@server.route("/")
def index():
    # go back to home page
    return flask.render_template("index.html")


@server.route("/call_back_1")
def call_back_1():
    print("call back used.")

    # go back to home page
    return flask.redirect("/")


@server.route("/store_file", methods = ["POST"])
def store_file():

    #storing the file here
    file_obj = flask.request.files["filename"]
    print(file_obj)
    file_obj.save("maintenance_file.csv")
    #return "Upload Successful"
    #return flask.redirect("/")
    return flask.render_template("index2.html")

@server.route('/sms_details')
def homepage():
    #Go back to homepage
    return render_template('index3.html')

@server.route('/message', methods = ["POST"])
def message():
     # Send a text message to the number provided

     message = client.messages.create(to=flask.request.form['phone_number'],
                                         from_='+12019043498',
                                         body=str(sms_content.message()))

     return flask.render_template("index2.html")

@server.route('/alarm', methods=['GET'])
def alarm():
    #Sends alarm when total power out is below 4MW
    value=4
    message = client.messages .create(body=str(sms_content.alarm(value)),
                         from_='+12019043498',
                         to='+2348032000142'
                     )
    return flask.render_template("index2.html")

app = dashboard.get_dash(server)

if __name__ == '__main__':
    app.run_server(port=5005, debug=True)
