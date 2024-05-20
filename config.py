"""
List of possible assitant parameters which form the request to the API
"""

###################
# Assistant Roles #
###################

teacher_assistant = {'role': 'assistant', 'content':
                     'A kind teacher who uses easy to understand words'}
korean_translation = {'role': 'assistant', 'content': 'A translator for a family friend'}


###################
# System Roles #
###################


##############
# User Roles #
##############

request_comment = {'role': 'user', 'content':
                    '''Write a 3-5 sentence summary of academic and behavior 
                    of the ESL student for their report cards.'''}
request_translation = {'role': 'user', 'content': 'Please translate this into Korean'}


##################
# Base Variables #
##################

MODEL = 'gpt-3.5-turbo'
MESSAGES = [
    teacher_assistant,
    request_comment,
]

TRANSLATION_MESSAGES = [
    korean_translation,
    request_translation
]
