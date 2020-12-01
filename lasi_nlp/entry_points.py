"""
Request to api

"""

## Imports
import requests
import ast
from json import dumps, loads
from datetime import datetime as dt

## Service URI
LASI_SERVICE = "http://localhost:5005"


## Classifier Class
class Classifier:
    """
    Main LASI nlp class. Requires token.

    """

    def __init__(self, token):
        
        self.lasi_api = lambda x : "{}/call/{}/{}".format(LASI_SERVICE, token, x)
        self.auth()

    def standarize(self, sentiment, reduce_neutral_proportion=1.25):
        neutral = sentiment["Neutral"]/reduce_neutral_proportion
        return {
            "Positive": (1-neutral)*(sentiment["Positive"]/(sentiment["Positive"]+sentiment["Negative"])),
            "Negative": (1-neutral)*(sentiment["Negative"]/(sentiment["Positive"]+sentiment["Negative"])),
            "Neutral": neutral
        }

    ## Classify
    def classify(self, text):
        """
        Get the emotions and sentiment of a text.
            Arguments:
                text (string or list of strings) - Text (or list of) to be classified.
        """
        payload = {'text':text}
        request = requests.post(self.lasi_api('combo'), data=dumps(payload))
        if request.status_code == 200:
            sentiment = ast.literal_eval(loads(request.text))['Sentiment']
            emotions = ast.literal_eval(loads(request.text))['Emotions']
            sentiment = [dict([a, float(x)] for a, x in b.items()) for b in sentiment]
            # hot fix
            sentiments  = []
            for sent in sentiment:
                sentiments.append(self.standarize(sent))
            emotions = [dict([a, float(x)] for a, x in b.items()) for b in emotions]
            return {'Sentiment' : sentiments, 'Emotions' : emotions}
        else:
            raise Exception(request.text)
    

    ## Auth
    def auth(self):
        """
        Get authentication status

        """

        request = requests.get(self.lasi_api('auth'))
        if request.status_code == 200:
            values = loads(loads(request.text))
            if values['authed'] == True:
                print('Authorized. Token Expiration: {}'.format(dt.fromisoformat(values['exp']).strftime("%d-%m-%Y")))
            else:
                print('Not authorized. Reason: {}'.format(values['reason']))
        else:
            raise Exception(request.text)
