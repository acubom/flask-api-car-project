from flask import Blueprint, request, jsonify
from cars_inventory.helpers import token_required
from cars_inventory.models import db, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

# CREATE DRONE ENDPOINT
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    color = request.json['color']
    condition = request.json['condition']    
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    price = request.json['price']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(year, make, model, color, condition, dimensions, weight, price, user_token = user_token)
    

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['POST'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    print(car)
    print(current_user_token)
    if car:
        car.year = request.json['year']
        car.make = request.json['make']
        car.model = request.json['model']
        car.color = request.json['color']
        car.condition = request.json['condition']    
        car.dimensions = request.json['dimensions']
        car.weight = request.json['weight']
        car.price = request.json['price']
        car.user_token = current_user_token.token
        db.session.commit()
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That car does not exist!'})
    
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That car does not exist!'})