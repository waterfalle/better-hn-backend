from json import dumps
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from src.stories import get_stories_v1, update_stories_v1
from src.data_store import data_store

APP = Flask(__name__)

# below code was taken from 
# https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
# this will run update_stories_v1 every 5 minutes AFTER sched.start()
sched = BackgroundScheduler(daemon=True)
sched.add_job(update_stories_v1,'interval',minutes=5)
sched.start()
# end of taken code

@APP.route("/stories", methods=["GET"])
def get_stories():
    num_stories = int(request.args.get('num_stories'))
    return dumps(get_stories_v1(num_stories))

if __name__ == "__main__":
    # initialise data_store
    data_store.__init__
    APP.run()


