from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopementConfig, TestingConfig
import keras
from object_detector import ObjectDetector

app = Flask(__name__)
app.config.from_object(DevelopementConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

model = ObjectDetector()



def create_app(testing_config = None):
    if testing_config != None:
        app.config.from_object(TestingConfig)
    return app


from models import Driver, Vehicle
import routes


if __name__ == "__main__":
    app.run()

