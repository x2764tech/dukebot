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
menu_url = 'https://raw.githubusercontent.com/duke-studios/cafeteria-data/master/menu.json'


# Hi world!
@slack.command('lunch', token=os.environ.get("SLACK_TOKEN_LUNCH"),
               team_id=os.environ.get("SLACK_TEAM_ID"), methods=['POST'],
               meal='lunch')
@slack.command('breakfast', token=os.environ.get("SLACK_TOKEN_BREAKFAST"),
               team_id=os.environ.get("SLACK_TEAM_ID"), methods=['POST'],
               meal='breakfast')
def meal_select(**kwargs):

    prefixes = [
        "I think you should try the",
        "I think you should have the",
        "You want to try the",
        "You want to have the",
        "Try the",
        "Have the",
        "I recommend the",
        "You want the",
        "My suggestion is the"
    ]

    suffixes = [
        "",
        " Delicious.",
        " Om nom nom!",
        " Bring me one as well!"
    ]

    response = urllib.urlopen(menu_url)
    data = json.loads(response.read())

    restriction = kwargs.get('text')

    item_diet_safe = False

    items = data[kwargs.get('meal')]['items']
    
    if restriction:
      items = [item for item in items if restriction in item['flags']]
    
    item = random.choice(items) 
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)

    text = "%s %s (%s).%s" % (prefix, item['name'], item['price'], suffix)

    return slack.response(
        text=text,
        response_type='in_channel')


# Fire it up!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
