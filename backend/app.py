from flask import Flask , jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_restplus import Api,Resource , fields 
from flask_cors import CORS
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 
app.config['SECRET_KEY']='619619'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api()
api.init_app(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','name','email','password')

model = api.model('model',{
    'name':fields.String('Enter name'),
    'email':fields.String('Enter name'),
    'password':fields.String('Enter name'),

})

users_schema = UserSchema(many=True)
user_schema = UserSchema()


@api.route('/get')
class get(Resource):
    def get(self):
        users = User.query.all()
        return jsonify(users_schema.dump(users))

@api.route('/post')
class post(Resource):
    @api.expect(model)
    def post(self):
        user = User(name=request.json['name'],email=request.json['email'],password=request.json['password'])
        db.session.add(user)
        db.session.commit()
        return {'message':'added to db'}
    
@api.route('/put/<int:id>')
class put(Resource):
    @api.expect(model)
    def put(self,id):
        user = User.query.get(id)
        user.name = request.json['name']
        user.email = request.json['email']
        user.password = request.json['password']
        db.session.commit()
        return {'message':'data updated'}

@api.route('/delete/<int:id>')
class delete(Resource):
    def delete(self,id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {'message':'deleted successfully'}


@api.route('/get/<int:id>')
class getone(Resource):
    def get(self,id):
        user = User.query.get(id)
        return jsonify(user_schema.dump(user))


if __name__ == '__main__':
    app.run(debug=True)