#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask
from flask_slack import Slack

app = Flask(__name__)

slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)


# Hi world!
@slack.command('hello', token=os.environ.get("SLACK_TOKEN"),
               team_id=os.environ.get("SLACK_TEAM_ID"), methods=['POST'])
def hello(**kwargs):
    text = kwargs.get('text')
    return slack.response(text)


# Fire it up!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
