from flask import request, jsonify, abort
from main import app
from models import Driver, Vehicle, DriverSchema, VehicleSchema
from main import db

from datetime import datetime


def convert_time(time):
    try:
        result = datetime.strptime(time, '%d-%m-%Y')
    except ValueError:
        abort(400, {'message': 'invalid date (ex. 20-12-2021)'})
    return result


@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description['message']})
    return response

@app.errorhandler(404)
def custom404(error):
    response = jsonify({'message': error.description['message']})
    return response



# Driver

@app.route('/drivers/driver', methods = ['GET'])
def get_list_drivers():

    if request.args.get('created_at__gte'):
        created_at__gte = request.args.get('created_at__gte')
        time = convert_time(created_at__gte)
        result = Driver.get_by_filter_time(time)

    elif request.args.get('created_at__lte'):
        created_at__lte = request.args.get('created_at__lte')
        time = convert_time(created_at__lte)
        result = Driver.get_by_filter_time(time, filter='lte')

    else:
        result = Driver.get_all()

    schema = DriverSchema()
    return {"drivers": schema.dump(result, many=True)}


@app.route('/drivers/driver', methods = ['POST'])
def create_driver():
    request_data = request.get_json()
    schema = DriverSchema()
    try:
        load_data = schema.load(request_data, session=db.session)
    except Exception as e:
        abort(400, {'message': str(e)})
    Driver.save(load_data)
    return schema.dump(load_data), 201


@app.route('/drivers/driver/<int:driver_id>', methods = ['GET'])
def get_driver(driver_id):
    driver = Driver.get_by_id(driver_id)
    if not driver:
        abort(404, {"message" : "Driver with id = {} not found".format(driver_id)})
    schema = DriverSchema()
    return {"driver" : schema.dump(driver)}


@app.route('/drivers/driver/<int:driver_id>', methods = ['PUT'])
def update_driver(driver_id):
    driver = Driver.get_by_id(driver_id)
    if not driver:
        abort(404, {"message" : "Driver with id = {} not found".format(driver_id)})

    schema = DriverSchema()
    request_data = request.get_json()

    driver.first_name = request_data.get('first_name', driver.first_name)
    driver.last_name = request_data.get('last_name', driver.last_name)

    Driver.save(driver)
    
    return {"update_driver" : schema.dump(driver)}

@app.route('/drivers/driver/<int:driver_id>', methods = ['DELETE'])
def delete_driver(driver_id):
    driver = Driver.get_by_id(driver_id)
    if not driver:
        abort(404, {"message" : "Driver with id = {} not found".format(driver_id)})

    Driver.delete(driver)
    
    return {"delete_driver" : "Driver with id = {} succeed remove".format(driver_id)}


# Vehicle

@app.route('/vehicles/vehicle/', methods = ['GET'])
def get_list_vehicles():
    if request.args.get('with_drivers'):
        with_drivers = request.args.get('with_drivers')
        if with_drivers not in ('yes', 'no'):
            abort(400, {'message': 'invalid paramater with_drivers (must be yes or no)'})
        result = Vehicle.get_with_drivers(with_drivers)
    else:
        result = Vehicle.get_all()
    
    schema = VehicleSchema()
    return {"vehicles": schema.dump(result, many=True)}


@app.route('/vehicles/vehicle/', methods = ['POST'])
def create_vehicle():
    request_data = request.get_json()
    schema = VehicleSchema()
    try:
        load_data = schema.load(request_data, session=db.session)
        Vehicle.save(load_data)
    except Exception as e:
        abort(400, {'message': str(e)})
    return schema.dump(load_data), 201

@app.route('/vehicles/vehicle/<int:vehicle_id>', methods = ['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.get_by_id(vehicle_id)
    if not vehicle:
        abort(404, {"message" : "Vehicle with id = {} not found".format(vehicle_id)})
    schema = VehicleSchema()
    return {"vehicle" : schema.dump(vehicle)}


@app.route('/vehicles/vehicle/<int:vehicle_id>', methods = ['PUT'])
def update_vehicle(vehicle_id):
    vehicle = Vehicle.get_by_id(vehicle_id)
    if not vehicle:
        abort(404, {"message" : "Vehicle with id = {} not found".format(vehicle_id)})

    schema = VehicleSchema()
    request_data = request.get_json()

    vehicle.driver_id = request_data.get('driver_id', vehicle.driver_id)
    vehicle.make = request_data.get('make', vehicle.make)
    vehicle.model = request_data.get('model', vehicle.model)
    vehicle.plate_number = request_data.get('plate_number', vehicle.plate_number)

    Vehicle.save(vehicle)
    
    return {"update_vehicle" : schema.dump(vehicle)}

@app.route('/vehicles/vehicle/<int:vehicle_id>', methods = ['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.get_by_id(vehicle_id)
    if not vehicle:
        abort(404, {"message" : "Vehicle with id = {} not found".format(vehicle_id)})

    Vehicle.delete(vehicle)
    
    return {"delete_driver" : "Vehicle with id = {} succeed remove".format(vehicle_id)}



@app.route('/vehicles/set_driver/<int:vehicle_id>', methods = ['POST'])
def put_or_drop_off_driver(vehicle_id):
    vehicle = Vehicle.get_by_id(vehicle_id)
    if not vehicle:
        abort(404, {"message" : "Vehicle with id = {} not found".format(id)})
    schema = VehicleSchema()
    if vehicle.driver_id == None:
        driver_id = Driver.get_driver_id_without_vehicle()
        if not driver_id:
            abort(200, {'message': 'Driver without vehicle not found'})
        vehicle.driver_id = driver_id
        action = "put_driver"
    else:
        vehicle.driver_id = None
        action = "drop_off_driver"
    Vehicle.save(vehicle)
    return {action : schema.dump(vehicle)}

    
    

    