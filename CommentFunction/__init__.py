import azure.functions as func
import json
from openai import OpenAI
import os
import config


def main(req: func.HttpRequest) -> func.HttpResponse:

    #############
    #  API KEY  #
    #############

    API_KEY = os.getenv('API_KEY')

    if not API_KEY:
        try:
            from chat_gpt_api_key import API_KEY
        except ImportError:
            return func.HttpResponse(
                json.dumps({                
                    'status': 'error',
                    'message': 'API Key not found.'
                }),
                status_code=400,
                mimetype='application/json'
            )
        
    #####################
    #  Initializations  #
    #####################

    client = OpenAI(api_key=API_KEY)

    ###########
    #  Route  #
    ###########

    ### Chat Route
    try:
        data = req.get_json()

        # Response requires a content and role field
        if 'role' not in data or 'content' not in data:
            return func.HttpResponse(
                json.dumps({                
                    'status': 'error',
                    'message': 'Missing required fields: role and content must be provided.'
                }),
                status_code=400,
                mimetype='application/json'
            )
    
        messages = config.messages.copy()
        messages.append(data)

        response = client.chat.completions.create(
            model = config.model,
            messages=messages
        )
        english_response = response.choices[-1].message.content
        

        translation_messages = config.translation_messages
        translation_messages.append({'role': 'user', 'content': english_response})


        translation = client.chat.completions.create(
            model=config.model,
            messages=translation_messages
        )
        korean_response = translation.choices[-1].message.content

        return func.HttpResponse(
            json.dumps({'English': english_response, 'Korean': korean_response}),
            status_code=200,
            mimetype='application/json'
        )
    
    except json.JSONDecodeError as e:
        return func.HttpResponse(
            json.dumps(
                {
                    'status': 'error',
                    'message': 'Invalid request.'
                },
                status_code=400,
                mimetype='application/json'
            )
        )