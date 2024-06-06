from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
from datetime import  datetime, date, timedelta


import os


dataforseo_email= os.environ.get('dataforseo_email')
dataforseo_password= os.environ.get('dataforseo_password')

class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
                ).decode("ascii")
            headers = {'Authorization' : 'Basic %s' %  base64_bytes, 'Content-Encoding' : 'gzip'}
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, 'POST', data_str)


client = RestClient(dataforseo_email, dataforseo_password)

def data_for_seo_queries(keyword: str, date_to:str|bool= None, date_from:str|bool= None):
    date_format= "%Y-%m-%d"
    if not date_to:
        date_to= date.today().__format__(date_format)
    if not date_from:
        one_year_ago= datetime.strptime(date_to, date_format)-timedelta(days=365)
        date_from= one_year_ago.date().__format__(date_format)
    error= None
    queries= []
    try:
        post_data = dict()
        post_data[len(post_data)] = dict(
                            location_name="United States",
                            date_from=date_from,
                            date_to=date_to,
                            keywords=[
                                keyword,
                            ],
                            item_types= [
                                "google_trends_queries_list"
                            ]
                        )
        response = client.post("/v3/keywords_data/google_trends/explore/live", post_data)
        if response['status_code']==20000:
            query_items= response['tasks'][0]['result'][0]['items'][0]['data']
            # top queries
            top_queries= query_items.get('top')
            if top_queries:
                for tq in top_queries:
                    queries.append(tq['query'])
            # rising queries
            rising_queries= query_items['rising']
            if rising_queries:
                for rq in rising_queries:
                    queries.append(rq['query'])    
    except Exception as e:
        print(e)
        error= e.__str__()
    finally:
        return {
            "error": error,
            "queries": queries
        }
        
# print(data_for_seo_queries("best headphones"))