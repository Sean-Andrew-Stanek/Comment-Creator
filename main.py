from flask import Flask, request, jsonify, render_template, session;
import os
import config
from openai import OpenAI

#############
#  API KEY  #
#############

API_KEY = os.getenv('API_KEY')

# Checks for the API key in the env and locally.  Otherwise stops.
if not API_KEY:
    try:
        from chat_gpt_api_key import API_KEY
    except ImportError:
        raise RuntimeError('API_KEY not found.  Either set your environment variable or create a file called chat_gpt_api_key.py and set your API_KEY there.')
    
#####################
#  Initializations  #
#####################

client = OpenAI(
    api_key=API_KEY
)

app = Flask(__name__, static_folder='static')

#############
#  Routes   #
#############

### Home Route
@app.route('/')
def home():
    return render_template('index.html')