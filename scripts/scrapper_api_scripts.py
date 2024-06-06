import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()


SCRAPPER_API_KEY= os.environ.get('SCRAPPER_API_KEY')
SCRAPPER_API_AMAZON_SEARCH_URL= os.environ.get('SCRAPPER_API_AMAZON_SEARCH_URL')
SCRAPPER_API_AMAZON_REVIEW_URL= os.environ.get('SCRAPPER_API_AMAZON_REVIEW_URL')


def get_ranking_products(search_query: str, num_results: int=5):
    payload = {
        'api_key': SCRAPPER_API_KEY, #add your API key here
        'query': search_query,
        'country': 'us'
    }
    results= []
    error=None
    try:
        response = requests.get(SCRAPPER_API_AMAZON_SEARCH_URL, params=payload)
        if response.ok:
            search_results= response.json()
            # unsorted list of results---> like they are ranked on amzon
            listed_results= search_results['results']
            # sorting results based on their reviews
            listed_results.sort(key= lambda x: x.get('total_reviews', 0), reverse=True)
            results= listed_results[:num_results]
                
        else:
            raise(f"Response from SCRAPPER: {response.status_code}")

    except Exception as e:
        print(e)
        error= e.__str__()
    finally:
        result= {
            'results':results,
            'error': error
        }
        return result
    
    
def get_review_of_product(asin: str, num_page_results: int=1):
    review_payload = {
        'api_key': SCRAPPER_API_KEY,
        'asin': asin,
        'country': 'us',
        'tld': 'com',
        # 'review_type': 'all',
        'review_type': 'avp_only_reviews', # applied verified purchase
        
    }
    results= []
    error=None
    try:
        response= requests.get(
                    SCRAPPER_API_AMAZON_REVIEW_URL,
                    params=review_payload
                )       
        if response.ok:
            reviews_results= response.json()
            results= reviews_results.get('reviews', [])
        else:
            raise(f"Response from SCRAPPER: {response.status_code}")

    except Exception as e:
        print(e)
        error= e.__str__()
    finally:
        result= {
            'reviews':results,
            'error': error
        }
        return result