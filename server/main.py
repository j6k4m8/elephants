import json

from flask import Flask, jsonify, request
from flask_cors import CORS


APP = Flask(__name__)
CORS(APP)



class ElephantManager:

    def __init__(self):
        self.elephants = {}
        self._since_clear_counter = 0
        self._reload()
        self._file = "elephantdb.json"

    def _reload(self):
        self._since_clear_counter += 1

        if self._since_clear_counter > 500:
            print("clearing all...")
            self.elephants = {}
            self._since_clear_counter = 0
            return
        try:
            self.elephants = json.load(open(self._file, 'r'))
        except:
            self.elephants = {}

    def _save(self):
        json.dump(self.elephants, open(self._file, 'w'))

    def peers(self, without=None, around: float = None):
        self._reload()
        if around is None:
            return {k: v for k, v in self.elephants.items() if k != without}

    def get_info(self, elephant_id: str):
        return self.elephants.get(elephant_id, {})

    def register_elephant(self, elephant_id, elephant):

        if elephant_id in self.elephants:
            saved_hue = self.elephants[elephant_id]["hue"]
        else:
            saved_hue = None

        if "currentX" not in elephant:
            print("current: " + str(elephant["currentX"]))
            return False
        try:
            elephant["currentX"] = float(elephant["currentX"])
        except:
            pass
        if not isinstance(elephant["currentX"], (float, int)):
            print("Bad type: " + str(type(elephant["currentX"])))
            return False

        if "targetX" not in elephant:
            print("target: " + str(elephant["targetX"]))
            return False
        try:
            elephant["targetX"] = float(elephant["targetX"])
        except:
            pass
        if not isinstance(elephant["targetX"], (float, int)):
            print("Bad type: " + str(type(elephant["targetX"])))
            return False

        if "hue" not in elephant:
            print("hue: " + str(elephant["hue"]))
            return False
        try:
            elephant["hue"] = float(elephant["hue"])
        except:
            pass
        if not isinstance(elephant["hue"], (float, int)):
            print("Bad type: " + str(type(elephant["hue"])))
            return False

        self.elephants[elephant_id] = elephant
        self._save()

        if saved_hue:
            return {
                "hue": saved_hue
            }
        else:
            return {}


EM = ElephantManager()


@APP.route("/")
def heartbeat():
    return jsonify({ "heartbeat": "ya im here" })


@APP.route("/peers/<elephant_id>", methods=["GET"])
def peers(elephant_id):
    elephant_id = request.access_route[-1] + elephant_id
    return jsonify(EM.peers(without=elephant_id))


@APP.route("/peer/<elephant_id>", methods=["GET"])
def peer_info(elephant_id: str):
    elephant_id = request.access_route[-1] + elephant_id
    return jsonify({
        "response": EM.get_info(elephant_id)
    })


@APP.route("/report/<elephant_id>", methods=["POST"])
def report(elephant_id: str):
    elephant_id = request.access_route[-1] + elephant_id
    return jsonify({
        "response": EM.register_elephant(elephant_id, request.json)
    })


if __name__ == "__main__":
    APP.run(host="0.0.0.0", debug=True, port=5050)
