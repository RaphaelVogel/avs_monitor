#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import utils
import random
import os
from requests.auth import HTTPBasicAuth

env_user = os.environ['user']
env_pwd = os.environ['pwd']
env_skill_id = os.environ['skill_id']
env_url = os.environ['url']

# ----------------------------------------------------------------------------------
# Events triggered from AVS
# ----------------------------------------------------------------------------------
def lambda_handler(event, context):
    # only call function, if it is triggered from my own skill
    if event['session']['application']['applicationId'] != env_skill_id:
        raise ValueError("Invalid Application ID")

    print("All incoming Event Details: " + str(event))

    # Create two main objects from 'event'
    session = event['session']
    request = event['request']

    # Session Attributes are used to track elements like current question details, last intent/function position, etc
    session_attributes = utils.load_session_attributes(session)
    print("Session Attributes: " + str(session_attributes))

    if session['new']:
        on_session_started({'requestId': request['requestId']}, session_attributes)

    if request['type'] == "LaunchRequest":
        return on_launch(request, session_attributes)
    elif request['type'] == "IntentRequest":
        return on_intent(request, session_attributes)
    elif request['type'] == "SessionEndedRequest":
        return on_session_ended(request, session_attributes)


def on_session_started(session_started_request, session_attributes):
    # Called when the session starts
    pass


def on_session_ended(session_ended_request, session_attributes):
    # Called when the user ends the session. Is not called when the skill returns should_end_session=true
    # add cleanup logic here
    pass


def on_launch(launch_request, session_attributes):
    # Called when the user launches the skill without specifying what they want
    return get_welcome_response(session_attributes)


def on_intent(intent_request, session_attributes):
    # Called when the user specifies an intent for this skill
    print("Intent Request Name: " + intent_request['intent']['name'])
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "firstBundesliga":
        requests.get(env_url + '/soccerTable/1',
                     auth=HTTPBasicAuth(env_user, env_pwd), verify=False)
        return utils.build_response({}, utils.build_speech_response(random.choice(utils.response_comments), True))
    elif intent_name == "secondBundesliga":
        requests.get(env_url + '/soccerTable/2',
                     auth=HTTPBasicAuth(env_user, env_pwd), verify=False)
        return utils.build_response({}, utils.build_speech_response(random.choice(utils.response_comments), True))
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return end_session()
    else:
        raise ValueError("Invalid intent")


# ----------------------------------------------------------------------------------
# Functions that control the skill's intent
# ----------------------------------------------------------------------------------
def get_welcome_response(session_attributes):
    speech_output = "<speak>Wilkommen, du kannst Infromationen auf dem Monitor im Wohnzimmer anzeigen lassen.</speak>"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "<speak>Folgende Befehle sind möglich:" \
                    "Tabelle der ersten Bundesliga anzeigen lassen." \
                    "Tabelle der zweiten Bundesliga anzeigen lassen.</speak>"
    should_end_session = False

    return utils.build_response(session_attributes,
        utils.build_speech_with_repromt_response(speech_output, should_end_session, reprompt_text))


# user wants to cancel or stop skill
def end_session():
    pass
