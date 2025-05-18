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
@app.route('/api/spaceship', methods =['GET'])

def display_spaceship():
    if 'id' in request.args:
        id = int(request.args['id'])
        
        #GET data by ID
        mycreds = creds.Creds()
        myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
        sql = "select * from spaceship"
        spaceship_data = execute_read_query(myconn, sql)
        spaceship_list = []
        for data in spaceship_data:
            if data['id'] == id:
                    spaceship_list.append(data)
        return jsonify(spaceship_list)
    

    else:
        #GET data by all
        mycreds = creds.Creds()
        myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
        sql = "select * from spaceship"
        spaceship_data = execute_read_query(myconn, sql)
        return jsonify(spaceship_data)
    

#POST API, Add new spaceship data. If captainid is not found on captain table, data will not add or update.         
@app.route('/api/spaceship', methods =['POST'])     
    
def add_spaceship():
    request_data = request.get_json()
    max_weight = request_data['maxweight']
    captain_id = request_data['captainid']

    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = "insert into spaceship (maxweight, captainid) values ('%s','%s')" % (max_weight, captain_id)
    execute_query(myconn , sql)

    return 'Add new spaceship info successfully'
    
#PUT API, use to update spaceship data base by ID via json.
@app.route('/api/spaceship', methods =['PUT']) 

def update_spaceship_data():
    request_data = request.get_json()
    ship_id = request_data['id']
    new_spaceship_maxweight = request_data['maxweight']
    new_captain_assign = request_data['captainid']

    mycreds = creds.Creds()
    myconnection = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = "UPDATE spaceship SET maxweight = '%s', captainid = '%s' WHERE id = %s" % (new_spaceship_maxweight, new_captain_assign, ship_id)

    execute_query(myconnection, sql)
    return f"Selected ship info with ID #{ship_id} updated successfully"    


#DELETE API, use to delete spaceship data.

@app.route('/api/spaceship', methods = ['DELETE'])

def delete_spaceship_data():
    request_data = request.get_json()
    delete_id = request_data['id']
    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = 'delete from spaceship where id = %s' % (delete_id)
    execute_query(myconn, sql)
    return "Delete spaceship request successful!"
    

app.run()