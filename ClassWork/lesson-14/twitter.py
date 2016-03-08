from TwitterAPI import TwitterAPI

#This has my credentials for my app
access_token_key = "oPGoeIBtOwzr0WvFszHDlD4FT"
access_token_secret = "nPoXFVdsNAD8seUQJfgikewoty0ZP5nQ8nA5WMLmZ63nCqwo0O"

api_key = "41222288-RekmlqkCyomXX1ruQNrxQYARUq2BDRp6cgyeY3hqK"
api_secret = "  ovfPxRdJyyGBwFt7tvYEtT3RVzk6pkpD6p0qv5PKrq4Y0"

_debug = 0

api = TwitterAPI(api_key, api_secret, access_token_key, access_token_secret)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''

def retrieve_tweets(topic, 
                    url="https://stream.twitter.com/1/statuses/filter.json", 
                    method="GET", ):
    """
    Params:
    topic - must be in this format "#topic" or '@handle"
    Returns
    """
    response = api.request('statuses/filter', {'track': topic})
    if response.status_code != 200:
        raise ValueError("Unable to retrieve tweets, please check your API credentials")
    for x in response:
        try:
            yield x
        except UnicodeError as unicode_error:
            continue