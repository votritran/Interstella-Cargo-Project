import flask
from flask import jsonify
from flask import request

import creds

from sql import create_connection
from sql import execute_read_query
from sql import execute_query

#create flask application
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#GET API
@app.route('/api/captain', methods =['GET'])

def display_captain():

    if 'id' in request.args:
        id = int(request.args['id'])
        
        #GET data by ID
        mycreds = creds.Creds()
        myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
        sql = "select * from captain"
        captain_data = execute_read_query(myconn, sql)
        captain_list = []
        for data in captain_data:
            if data['id'] == id:
                    captain_list.append(data)
        return jsonify(captain_list)
    

    else:
        #GET data by all
        mycreds = creds.Creds()
        myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
        sql = "select * from captain"
        captain_data = execute_read_query(myconn, sql)
        return jsonify(captain_data)
    
#POST API, Add new captain data.         
@app.route('/api/captain', methods =['POST'])     
    
def add_captain():
    request_data = request.get_json()
    first_name = request_data['firstname']
    last_name = request_data['lastname']
    user_rank = request_data['ranks']
    homeplanet = request_data['homeplanet']

    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = "insert into captain (firstname, lastname, ranks, homeplanet) values ('%s','%s', '%s', '%s')" % (first_name, last_name, user_rank, homeplanet)
    execute_query(myconn , sql)

    return 'Add new captain info successfully'

#PUT API, use to update captain data base.
@app.route('/api/captain', methods =['PUT']) 

def update_captain_data():
    request_data = request.get_json()
    data_id = request_data['id']
    new_first_name = request_data['firstname']
    new_last_name = request_data['lastname']
    new_rank = request_data['ranks']
    new_homeplanet = request_data['homeplanet']

    mycreds = creds.Creds()
    myconnection = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = "UPDATE captain SET firstname = '%s', lastname = '%s', ranks = '%s', homeplanet = '%s' WHERE id = %s" % (new_first_name, new_last_name, new_rank, new_homeplanet, data_id)

    execute_query(myconnection, sql)
    return f"Selected captain info with ID {data_id} updated successfully"


#DELETE API, use to delete captain data.

@app.route('/api/captain', methods = ['DELETE'])

def delete_captain_data():
    request_data = request.get_json()
    delete_id = request_data['id']
    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = 'delete from captain where id = %s' % (delete_id)
    execute_query(myconn, sql)
    return "Delete request successful!"


app.run()