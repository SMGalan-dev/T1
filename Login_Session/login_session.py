from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['MONGO_DBNAME'] = 'TEST1'
app.config['MONGO_URI'] = 'mongodb+srv://TEST1:password1.@test-mlktz.mongodb.net/test'

mongo = PyMongo(app)

@app.route('/')
def index():
    output = []
    if 'name' in session:
        return 'You are logged in as ' + session['name']

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.json['name']})
    if login_user:
        if request.json['password'].encode('utf-8') == login_user['password'].encode('utf-8'):
            session['name'] = request.json['name']
            output = {'name' : login_user['name']}
        else:
            output = 'Invalid name/password combination'

    else:
        output = 'The username doesnt exist'

    return jsonify({'login' : output})


@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    existing_user = users.find_one({'name' : request.json['name']})

    if existing_user is None:
        user_id = users.insert({'name' : request.json['name'], 'password' : request.json['password']})
        new_user = users.find_one({'_id' : user_id})
        output = {'name' : new_user['name']}    
    else:
        output = 'That username already exists'  

    return jsonify({'register' : output})

@app.route('/delete/<string:name>', methods=['DELETE'])
def remove_one(name):
    users = mongo.db.users
    delete_user = users.find_one({'name' : name})

    if delete_user is None:
        output = 'That username doesnt exists' 
    else: 
        users.remove(delete_user)
        output = {'name' : delete_user['name']}

    return jsonify({'deleted' : output})
    #return "Deleted: {} \n".format(delete_user)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)