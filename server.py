import threading
import time
from json import dumps
from flask import Flask, request
from src.stories import get_stories_v1, update_stories_v1
from src.data_store import data_store

APP = Flask(__name__)

@APP.route("/stories", methods=["GET"])
def get_stories():
    num_stories = int(request.args.get('num_stories'))
    return dumps(get_stories_v1(num_stories))

def updater():
    '''
    This function will be in another thread, and will periodically call
    the update_stories_v1() function to update the top stories.
    '''
    while True:
        update_stories_v1()
        time.sleep(300)

if __name__ == "__main__":
    # initialise data_store
    data_store.__init__
    # create thread for updater()
    # thread = threading.Thread(target=updater).start()
    update_stories_v1()
    APP.run()


