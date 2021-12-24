from main import db
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Driver(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    vehicles = db.relationship('Vehicle', backref='driver')


    @classmethod
    def get_all(cls):
        return cls.query.all()
    

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get(id)


    @classmethod
    def get_by_filter_time(cls, time, filter = 'gte'):
        if filter == 'gte':
            result = cls.query.filter(cls.created_at >= time).all()
        else:
            result = cls.query.filter(cls.created_at <= time).all()
        return result

    @classmethod
    def get_driver_id_without_vehicle(cls):
        return cls.query.filter(cls.vehicles == None).one().id


    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return '<Driver %r>' % self.first_name


class Vehicle(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))

    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    plate_number = db.Column(db.String(10), unique=True, nullable=False)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)#get_or_404(id)

    @classmethod
    def get_with_drivers(cls, with_drivers):
        if with_drivers == 'yes':
            result = cls.query.filter(cls.driver_id != None).all()
        else:
            result = cls.query.filter(cls.driver_id == None).all()
        return result

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return '<Vehicle %r>' % self.plate_number



class DriverSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Driver
        include_relationships = True
        load_instance = True


class VehicleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        include_fk = True
        load_instance = True