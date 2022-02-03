from flask import Flask
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)


class travelTime(Resource):
    def get(self, distance, timeWithNoStop, autonomy, reloadTime):
        #vitesse moyenne 78kmh
        #todo, call another API for real speed on a track
        res =  timeWithNoStop + (autonomy//distance)*reloadTime
        return {"Result": res}


api.add_resource(travelTime, '/traveltime/<int:distance>/<int:timeWithNoStop>/<int:autonomy>/<int:reloadTime>')

if __name__ == '__main__':
    app.run(debug=True)