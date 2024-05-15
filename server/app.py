from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_list = [{"id": plant.id, "name": plant.name} for plant in plants]
        return jsonify(plant_list)

    def post(self):
        data = request.get_json()
        name = data.get("name")
        image = data.get("image")
        price = data.get("price")
        plant = Plant(name=name, image=image, price=price)
        db.session.add(plant)
        db.session.commit()
        return jsonify({"message": "Plant created successfully"}), 201


api.add_resource(Plants, "/plants")


class PlantByID(Resource):
    pass


if __name__ == "__main__":
    app.run(port=5555, debug=True)
