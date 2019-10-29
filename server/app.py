from flask import Flask
from flask_restful import Api, Resource, reqparse
from collections import namedtuple

import time

app = Flask(__name__)
api = Api(app)

Identity = namedtuple("Identity", ["value", "timestamp"])

active_ids = [
]

expiry_time = 120

def is_expired(i):
    return (time.time() - i.timestamp) > expiry_time

class ID(Resource):
    def get(self, desired):
        print(active_ids)
        if desired > 0 and desired < len(active_ids):
            active_ids[desired] = active_ids[desired]._replace(timestamp = time.time())
            return desired, 200
        for i in range(len(active_ids)):
            if is_expired(active_ids[i]):
                active_ids[i] = active_ids[i]._replace(timestamp = time.time())
                return active_ids[i].value, 200
        last_val = active_ids[-1].value + 1 if len(active_ids) > 0 else 0
        new_id = Identity(value=last_val, timestamp=time.time())
        active_ids.append(new_id)
        return new_id.value, 200
      
api.add_resource(ID, "/id/<int:desired>")

app.run(host="0.0.0.0")
