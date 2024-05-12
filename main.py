from flask import Flask, request, jsonify, render_template, make_response;
import json
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

### Chat Route
@app.route('/comment', methods=['POST'])
def makeComment():

    try:
        data = request.get_json()

        # Response required to meet format    
        if 'role' not in data or 'content' not in data:
            error_response = {
                'status': 'error',
                'message': 'Missing required fields: role and content must be provided.'
            }
            return make_response(jsonify(error_response), 400)
        
        messages = config.messages
        messages.append(data)

        response = client.chat.completions.create(
            model = config.model,
            messages=messages
        )
        english_response = response.choices[-1].message.content
        print(english_response);

        translation_messages = config.translation_messages
        translation_messages.append({'role': 'user', 'content': english_response})


        translation = client.chat.completions.create(
            model=config.model,
            messages=translation_messages
        )

        return_message = jsonify({'English': english_response, 'Korean': translation.choices[-1].message.content})
        print(return_message)
        return make_response(return_message, 200)
    
    except json.JSONDecodeError:
        error_response = {
            'status': 'error',
            'message': 'Invalid request.'
        }
        return make_response(jsonify(error_response), 400)
        
if __name__ == '__main__':
    app.run(debug=True)

            
    



