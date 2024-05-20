"""
This module containes an Azure Function which processes HTTP requests.
The function will respond to an object
and return a new response from the OpenAI API based on parameters found
within the config.py file.
"""

import json
import os
import azure.functions as func
from openai import OpenAI
import config
from chat_gpt_api_key import API_KEY


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    This function handles the request.
    It extracts parameters and descriptions from a single message to make a new API request.
    It returns an English and Korean translation of the requested comment

    Args: 
        req (funct.HttpRequest):
            JSON object:
                role: always needs to be "user"
                content: description of student's name, behavior, etc
        
    Returns:
        func.HttpResponse:
            JSON object:
                English: Response in English
                Korean: Response in Korean

    """


    #############
    #  API KEY  #
    #############

    api_key = os.getenv('API_KEY')

    if not api_key:
        try:
            api_key=API_KEY
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

    client = OpenAI(api_key=api_key)

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

        messages = config.MESSAGES.copy()
        messages.append(data)

        response = client.chat.completions.create(
            model = config.MODEL,
            messages=messages
        )
        english_response = response.choices[-1].message.content

        translation_messages = config.TRANSLATION_MESSAGES
        translation_messages.append({'role': 'user', 'content': english_response})


        translation = client.chat.completions.create(
            model=config.MODEL,
            messages=translation_messages
        )
        korean_response = translation.choices[-1].message.content

        return func.HttpResponse(
            json.dumps({'English': english_response, 'Korean': korean_response}),
            status_code=200,
            mimetype='application/json'
        )

    except json.JSONDecodeError:
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
    