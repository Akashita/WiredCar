from flask import Flask
from flask_restful import Resource, Api, abort
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, ressources={r"/traveltime*": {"origins": "*"}})
api = Api(app)


class travelTime(Resource):
    def get(self, stops, timeWithNoStop, reloadTime):
        time =  timeWithNoStop + (stops * reloadTime)
        hours = time / 3600
        minu = (time % 3600) / 60
        resStr = str(int(hours)) + "h" + str(int(minu))
        if(((time % 3600) % 60)/10 == 0):
            resStr = resStr + "0"
        return {"traveltime": resStr}


api.add_resource(travelTime, '/traveltime/<int:stops>/<int:timeWithNoStop>/<int:reloadTime>')

if __name__ == '__main__':
    app.run(debug=True)