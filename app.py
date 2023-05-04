import csv
import random

import werkzeug
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager,jwt_required,create_access_token
import os


app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir,'users.db')
app.config['JWT_SECRET_KEY']='super-secret'


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')

@app.cli.command('db_seed')
def db_seed():
    uthpala = User(f_name='uthpala',
                   l_name='bandara',
                   email='lekam@gmail.com',
                   password='uthpala@123')


    chamodya = User(f_name='chamodya',
                   l_name='lekam',
                   email='bandara@gmail.com',
                   password='chamodya@123')

    db.session.add(uthpala)
    db.session.add(chamodya)
    db.session.commit()
    print('Database seeded')


@app.route('/')
def home():
    return render_template('SlashView.html')
@app.route('/loginview.html')
def login():
    return render_template('loginview.html')

@app.route('/login', methods=['POST'])
def login_user():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        print(access_token)
        return render_template('Menu.html')
        print("login succeeded")
    else:
        return render_template('loginview.html')

@app.route('/StoreEnd.html')
def StoreAdd():
    return render_template('StoreEnd.html')

@app.route('/StoreView.html')
def StoreView():
    with open('form_data.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return render_template('StoreView.html', data=data)
@app.route('/submit-form', methods=["POST"])
def storeend():
    id = random.randint(1, 1000)
    gender = request.form['field1']
    masterCategory = 'Apparel'
    subCategory = request.form['field2']
    articleType = request.form['field3']
    baseColour = request.form['field4']
    season = request.form['field5']
    year = 2023
    usage = request.form['field6']
    productDisplayName = request.form['field7']
    image = request.files['image']
    filename = werkzeug.utils.secure_filename(image.filename)
    image.save("./Database/" + filename)
    imagepath = "./Database/" +filename


    data ={'id': id,'gender': gender,'masterCategory': masterCategory, 'subCategory': subCategory,'articleType': articleType,'baseColour': baseColour,'season': season ,'year': year,'usage': usage,'productDisplayName': productDisplayName, 'image':imagepath}
    with open('form_data.csv', mode='a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['id','gender','masterCategory', 'subCategory','articleType','baseColour','season','year','usage','productDisplayName', 'image'])
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

    print(gender,subCategory,articleType,baseColour,season,usage,productDisplayName)
    return render_template('Menu.html')

@app.route('/uploadimage', methods=["POST"])
def uploadimage():
    if(request.method == "POST"):
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save("./UploadedImage/" + filename)
        # imagefile.save("./UploadedImage/" + filename)
        return jsonify({
            "message": "Image Uploaded Successfully"
        })

@app.route('/uploadtext', methods=["POST"])
def uploadtext():
    if(request.method == "POST"):
        data = request.get_json()
        gender = data['gender']
        print(gender)
        return jsonify({
            "message":"Text Uploaded "
        })

@app.route('/testurl', methods=["POST"])
def testurl():
    if(request.method == "POST"):
        data = request.get_json()
        name = data['name']
        email = data['email']
        response = {
            'status': 'success',
            'name': name,
            'email': email
        }
        return jsonify(response)




#database models
class User(db.Model):
    tablename ='Users'
    id = Column(Integer,primary_key=True)
    f_name = Column(String)
    l_name =Column(String)
    email = Column(String,unique=True)
    password = Column(String)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','f_name','l_name','email','password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)



if __name__ == '__main__':
    app.run()
