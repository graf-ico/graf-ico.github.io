from database import DB

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)


class AllGroups(Resource):
    def get(self):
        # Connect to databse
        db = DB()

        # Perform query and return JSON data
        return db.getAllTelegramGroups()


class Overlaps(Resource):
    def get(self, group):
        # Connect to databse
        db = DB()

        groupDetails = db.getTelegramGroup(group)

        if groupDetails == None:
            return {"error": "no data for group"}

        # Perform query and return JSON data
        return db.getOverlaps(group)


api.add_resource(Overlaps, '/overlaps/<string:group>')
api.add_resource(AllGroups, '/groups')

if __name__ == '__main__':
    app.run()
