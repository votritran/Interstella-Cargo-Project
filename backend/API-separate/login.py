import hashlib
import datetime
import time
import flask
from flask import jsonify
from flask import request, make_response


app = flask.Flask(__name__)
app.config['DEBUG'] = True

masterPassword = "cddd67830982a78cc83998c15c13e49e1cb6bea286c4507cb5510d9c6aba4ec3" #Hash value of 'tri'
masterUsername = 'username'

#BASIC AUTHENTICATION FROM HASHING
@app.route('/login', methods=['GET'])

def auth_test():
    if request.authorization:
        encoded = request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> Authorized user access </h1>'
    
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

#test this
app.run()