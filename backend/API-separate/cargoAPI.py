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
@app.route('/api/cargo', methods =['GET'])

def display_cargo():

    if 'id' in request.args:
        id = int(request.args['id'])
        
        #GET cargo data by ID
        mycreds = creds.Creds()
        myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
        sql = "select * from cargo"
        cargo_data = execute_read_query(myconn, sql)
        cargo_list = []
        for data in cargo_data:
            if data['id'] == id:
                    cargo_list.append(data)
        return jsonify(cargo_list)
    

    else:
        #GET data by all
        mycreds = creds.Creds()
        myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
        sql = "select * from cargo"
        cargo_data = execute_read_query(myconn, sql)
        return jsonify(cargo_data)
    
#POST API, Add new cargo data.         
@app.route('/api/cargo', methods =['POST'])     
    
def add_cargo():
    request_data = request.get_json()
    cargo_weight = request_data['weight']
    cargo_type = request_data['cargotype']
    departure_date= request_data['departure']
    arrival_date = request_data['arrival']
    ship_id = request_data['shipid']

    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = "insert into cargo (weight, cargotype, departure, arrival, shipid) values ('%s','%s', '%s', '%s', '%s')" % (cargo_weight, cargo_type,departure_date, arrival_date, ship_id)
    execute_query(myconn , sql)

    return 'Add new cargo info successfully'

#PUT API, use to update Cargo data base.
@app.route('/api/cargo', methods =['PUT']) 

def update_cargo_data():
    request_data = request.get_json()
    cargo_id = request_data['id']
    new_weight = request_data['weight']
    new_cargotype = request_data['cargotype']
    new_departure = request_data['departure']
    new_arrival = request_data['arrival']
    new_shipid = request_data['shipid']

    mycreds = creds.Creds()
    myconnection = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = "UPDATE cargo SET weight = '%s', cargotype = '%s', departure = '%s', arrival = '%s', shipid = '%s' WHERE id = %s" % (new_weight, new_cargotype, new_departure, new_arrival, new_shipid,cargo_id)

    execute_query(myconnection, sql)
    return f"Selected Cargo info with ID {cargo_id} updated successfully"


#DELETE API, use to delete cargo data.

@app.route('/api/cargo', methods = ['DELETE'])

def delete_cargo_data():
    request_data = request.get_json()
    delete_id = request_data['id']
    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    sql = 'delete from cargo where id = %s' % (delete_id)
    execute_query(myconn, sql)
    return f"Delete Cargo with ID {delete_id} request successful!"

app.run()

