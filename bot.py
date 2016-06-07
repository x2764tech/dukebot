#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask
from flask_slack import Slack
import random
import urllib
import json


# Let's get a Flask app going
app = Flask(__name__)
slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)


# Configuration!
# Where can we find the menu?
menu_url = 'https://raw.githubusercontent.com/duke-studios/cafeteria-data/master/opening-hours.json'


# Hi world!
@slack.command('lunch', token=os.environ.get("SLACK_TOKEN"),
               team_id=os.environ.get("SLACK_TEAM_ID"), methods=['POST'])
def lunch(**kwargs):

    prefixes = [
        "I think you should try the",
        "You want to have the",
        "Why not try the",
        "I recommend the",
        "You want the",
        "My suggestion is the"
    ]

    response = urllib.urlopen(menu_url)
    data = json.loads(response.read())

    item = random.choice(data['lunch']['items'])
    prefix = random.choice(prefixes)
    text = "%s %s (%s)." % (prefix, item['name'], item['price'])

    return slack.response(
        text=text,
        response_type='in_channel')


# Fire it up!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
