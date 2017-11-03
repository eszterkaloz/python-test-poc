from flask import Flask, request, jsonify
from models import db
from schemas import user_schema
from authorization import authorize
import escher_validator


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def activate_job():
    db.create_all()


@app.route('/', methods=['GET'])
def test():
    return 'Hello Pisti!'


@app.route('/greet/<name>', methods=['GET'])
def greet(name):
    return 'Hello %s!' % name


@app.route('/user', methods=['POST'])
def create_user():
    user = user_schema.load(request.get_json(), session=db.session).data
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user).data)


@app.route('/auth-test', methods=['GET'])
@authorize(escher_validator.validate_request)
def auth_test():
    return 'OK ;-)'


if __name__ == "__main__":
    app.run(port=5000, debug=True)
