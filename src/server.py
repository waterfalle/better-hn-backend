import pickle
from json import dumps
from flask import Flask, request
from src.stories import get_stories_v1
from src.stories import update_stories_v1
from src.data_store import data_store

APP = Flask(__name__)

@APP.route("/stories", methods=["GET"])
def get_stories():
    num_stories = int(request.args.get('num_stories'))
    return dumps(get_stories_v1(num_stories))

if __name__ == "__main__":
    # try:
    #     with open('database.p', 'rb') as FILE:
    #         store = pickle.load(FILE)
    #         data_store.set(store)
    # except FileNotFoundError:
    #     data_store.__init__
    data_store.__init__
    update_stories_v1()
    APP.run(port=2000, debug=True)

