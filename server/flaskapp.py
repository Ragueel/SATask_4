from flask import jsonify, request, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import json
import os

DB_ADDRESS = os.environ.get('DB_ADDRESS', 'sa.database:31792')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'master-password')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:{0}@{1}/postgres".format(DB_PASSWORD,DB_ADDRESS)
db = SQLAlchemy(app)

class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def toJson(self):
        return {'name': self.name, 'userId':'user_id'}


@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Hello, world!"

@app.route('/getAll')
def get_users():
    all_users = UserModel.query.all()
    return json.dumps({'response':[x.toJson() for x in allUsers]})

@app.route('/deleteUser')
def delete_user():
    data = request.args

    found_user = UserModel.query.filter_by(name=data.get('name','')).first()

    if found_user is not None:
        db.session.delete(found_user)
        db.session.commit()
        return json.dumps({'status': 'Updated'})

    return json.dumps({'status':'not found'})

@app.route('/updateUser')
def update_user():
    data = request.args

    found_user = UserModel.query.filter_by(name=data.get('name','')).first()

    if found_user is not None:
        found_user.name = ''
        db.session.commit()

        return json.dumps({'status': 'Updated'})
    return json.dumps({'status': 'not found'})

@app.route("/create", methods=["POST"])
def add_user():
    data = request.args

    new_user = UserModel(name=data.get('name',''))
    db.session.add(new_user)

    db.session.commit()
    return json.dumps(new_user.toJson())



if __name__ == "__main__":
    db.create_all()
    sample_user = UserModel(name='Sample')
    db.session.add(sample_user)
    sample_user = UserModel(name='Sample 2')
    db.session.add(sample_user)
    db.session.commit()
    allUsers = UserModel.query.all()

    app.run(host="0.0.0.0", port=5000)