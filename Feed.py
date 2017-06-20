import requests

from pip._vendor import requests


class GetRequests:

    market_list = {}


    #Skapa dictionary med alla marknader id + namn
    def create_market_list(self, session_key1, headers):
        r =requests.get('https://api.test.nordnet.se/next/2/markets',
        auth=(session_key1, session_key1), headers=headers)
        response_json = r.json()
        print("***************'")

        for i in response_json:
            name_str = i['name']
            market_id = i['market_id']
            self.market_list[market_id] = name_str


    def instrument_name(self, session_key1, headers, name):
        r =requests.get('https://api.test.nordnet.se/next/2/instruments?query='+name+'&type=A&country=SE',
        auth=(session_key1, session_key1), headers=headers)
        response_json = r.json()
        print("**********lklklk*****'")
        print(response_json)
        print('slut!')



