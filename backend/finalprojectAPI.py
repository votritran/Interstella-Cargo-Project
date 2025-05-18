import flask
import hashlib
from flask import jsonify
from flask import request, make_response

import creds

from sql import create_connection
from sql import execute_read_query
from sql import execute_query

#create flask application
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#LOGIN AUTHENTICATION

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

#GET CAPTAIN API
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
    first_name = request_data['selectfname']
    last_name = request_data['selectlname']
    new_first_name = request_data['firstname']
    new_last_name = request_data['lastname']
    new_rank = request_data['ranks']
    new_homeplanet = request_data['homeplanet']

    mycreds = creds.Creds()
    myconnection = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    cursor = myconnection.cursor(dictionary=True)

     # Check if the captain exists using a parameterized query
    sql_check = "SELECT id FROM captain WHERE firstname = %s AND lastname = %s"
    cursor.execute(sql_check, (first_name, last_name))
    check_complete = cursor.fetchone()  # Fetch one record

    if check_complete:
        # Update the captain's information using a parameterized query
        sql_update = """
            UPDATE captain 
            SET firstname = %s, lastname = %s, ranks = %s, homeplanet = %s 
            WHERE id = %s
        """
        cursor.execute(sql_update, (new_first_name, new_last_name, new_rank, new_homeplanet, check_complete['id']))
        myconnection.commit()  # Commit the changes

        return "Update Successful"
    else:
        return "Update unsuccessful"


#DELETE API, use to delete captain data.

@app.route('/api/captain', methods = ['DELETE'])

def delete_captain_data():
    request_data = request.get_json()
    first_name = request_data['firstname']
    last_name = request_data['lastname']
    mycreds = creds.Creds()
    myconnection = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    cursor = myconnection.cursor(dictionary=True)
    sql_delete = 'DELETE from captain WHERE firstname = %s AND lastname = %s'
    cursor.execute(sql_delete, (first_name, last_name))
    myconnection.commit()
    if cursor.rowcount > 0:
        return "delete successful"
    else:
        return "Delete unsuccessful"

#GET CARGO API
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
                    data['departure'] = data['departure'].strftime('%Y-%m-%d')
                    data['arrival'] = data['arrival'].strftime('%Y-%m-%d')
                    cargo_list.append(data)
        return jsonify(cargo_list)
    

    else:
        #GET data by all
        mycreds = creds.Creds()
        myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
        sql = "select * from cargo"
        cargo_data = execute_read_query(myconn, sql)
        cargo_list = []
        for data in cargo_data:
            data['departure'] = data['departure'].strftime('%Y-%m-%d')
            data['arrival'] = data['arrival'].strftime('%Y-%m-%d')
            cargo_list.append(data)

        return jsonify(cargo_list)
    
#POST API, Add new cargo data.         
@app.route('/api/cargo', methods =['POST'])     
    
def add_cargo():
    request_data = request.get_json()
    cargo_weight = request_data['weight']
    cargo_id = request_data['cargo_id'].upper()
    cargo_type = request_data['cargotype']
    departure_date= request_data['departure']
    arrival_date = request_data['arrival']
    shipname = request_data['shipname']

    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    cursor = myconn.cursor(dictionary=True)

     # Check if the captain exists using a parameterized query
    try:
        sql_check = "SELECT id FROM spaceship WHERE shipname = %s"
        cursor.execute(sql_check, (shipname,))
        check_complete = cursor.fetchone()  # Fetch one record

        if check_complete:
            sql_add = "INSERT INTO cargo (cargo_id, cargotype, shipname, weight, departure, arrival, shipid) values (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_add, (cargo_id, cargo_type, shipname, cargo_weight, departure_date, arrival_date, check_complete['id']))
            myconn.commit()

            return 'Add new cargo info successfully'
        else:
            return 'Add new Cargo unsucessful'
        
    except Exception as e:
        return "Error Occur"

    finally:
        # Close the cursor and connection
        cursor.close()
        myconn.close()


#PUT API, use to update Cargo data base.
@app.route('/api/cargo', methods =['PUT']) 

def update_cargo_data():
    request_data = request.get_json()
    cargo_id = request_data['cargo_id'].upper()
    new_weight = request_data['weight']
    new_cargotype = request_data['cargotype']
    new_departure = request_data['departure']
    new_arrival = request_data['arrival']
    new_shipname = request_data['shipname']

    mycreds = creds.Creds()
    myconnection = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    cursor = myconnection.cursor(dictionary=True)

    try:
        sql_check = "SELECT id FROM spaceship WHERE shipname = %s"
        cursor.execute(sql_check, (new_shipname,))
        check_complete = cursor.fetchone()  # Fetch one record

        if check_complete:
            sql_update = "UPDATE cargo SET cargotype = %s , shipname = %s , weight = %s, departure=%s, arrival= %s, shipid = %s WHERE cargo_id = %s"
            cursor.execute(sql_update, (new_cargotype, new_shipname, new_weight, new_departure, new_arrival, check_complete['id'], cargo_id))
            myconnection.commit()
            return 'Update new cargo info successfully'
        else:
            return 'Update new Cargo unsucessful'
        
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

    finally:
        # Close the cursor and connection
        cursor.close()
        myconnection.close()

#DELETE API, use to delete cargo data.

@app.route('/api/cargo', methods = ['DELETE'])

def delete_cargo_data():
    request_data = request.get_json()
    delete_id = request_data['cargo_id'].upper()
    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    cursor = myconn.cursor(dictionary=True)

    try:
        sql_check = "SELECT id FROM cargo WHERE cargo_id = %s"
        cursor.execute(sql_check, (delete_id,))
        check_complete = cursor.fetchone()  # Fetch one record

        if check_complete:
            sql_delete = 'delete from cargo where id = %s'
            cursor.execute(sql_delete,(check_complete['id'],))
            myconn.commit()
            return 'delete cargo info successfully'
        else:
            return 'delete Cargo unsucessful'
        
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

    finally:
        # Close the cursor and connection
        cursor.close()
        myconn.close()

#GET SPACESHIP API
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
    first_name = request_data['captainfname']
    last_name = request_data['captainlname']
    ship_name = request_data['shipname']

    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    cursor = myconn.cursor(dictionary=True)

     # Check if the captain exists using a parameterized query
    try:
        sql_check = "SELECT id FROM captain WHERE firstname = %s AND lastname = %s"
        cursor.execute(sql_check, (first_name, last_name))
        check_complete = cursor.fetchone()  # Fetch one record

        if check_complete:
            sql_add = "INSERT INTO spaceship (maxweight, shipname, captainfname, captainlname, captainid) values (%s,%s,%s,%s,%s)"
            cursor.execute(sql_add, (max_weight, ship_name, first_name, last_name, check_complete['id']))
            myconn.commit()

            return 'Add new spaceship info successfully'
        else:
            return 'Add spaceship unsucessful'
        
    except Exception as e:
        return "Unsuccessful"

    finally:
        # Close the cursor and connection
        cursor.close()
        myconn.close()
    
#PUT API, use to update spaceship data base by ID via json.
@app.route('/api/spaceship', methods =['PUT']) 

def update_spaceship_data():
    request_data = request.get_json()
    ship_name = request_data['shipname']
    new_spaceship_maxweight = request_data['maxweight']
    new_spaceship_name = request_data['newshipname']
    new_captain_fname = request_data['captainfname']
    new_captain_lname = request_data['captainlname']

    mycreds = creds.Creds()
    myconnection = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    cursor = myconnection.cursor(dictionary=True)
    # Check if the captain exists using a parameterized query
    try:
        sql_check = "SELECT id FROM captain WHERE firstname = %s AND lastname = %s"
        cursor.execute(sql_check, (new_captain_fname, new_captain_lname))
        check_complete = cursor.fetchone()  # Fetch one record
        if check_complete:
            sql_update = "UPDATE spaceship SET maxweight = %s, shipname = %s, captainfname = %s, captainlname = %s, captainid = %s WHERE shipname = %s"
            cursor.execute(sql_update,(new_spaceship_maxweight, new_spaceship_name, new_captain_fname, new_captain_lname, check_complete['id'], ship_name))
            myconnection.commit()
            return 'update new spaceship info successfully'

        else:
            return 'update spaceship unsucessful'
        
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

    finally:
        # Close the cursor and connection
        cursor.close()
        myconnection.close()


#DELETE API, use to delete spaceship data.

@app.route('/api/spaceship', methods = ['DELETE'])

def delete_spaceship_data():
    request_data = request.get_json()
    delete_id = request_data['shipname']
    mycreds = creds.Creds()
    myconn = create_connection(mycreds.connectionlink, mycreds.username, mycreds.passwd, mycreds.dataBase)
    cursor = myconn.cursor()
    try:
         # Check if the spaceship exists before trying to delete it
        sql_check = "SELECT shipname FROM spaceship WHERE shipname = %s"
        cursor.execute(sql_check, (delete_id,))
        spaceship_exists = cursor.fetchone()

        if spaceship_exists:
            # Use parameterized query for the DELETE statement
            sql_delete = "DELETE FROM spaceship WHERE shipname = %s"
            cursor.execute(sql_delete, (delete_id,))
            myconn.commit()  # Commit the changes
            return "Delete spaceship successful"
        else:
            return "delete unsuccessful"
    except Exception as e:
        return jsonify({"message": "An error occurred: " + str(e)}), 500

    finally:
        # Close the cursor and connection
        cursor.close()
        myconn.close()


app.run()