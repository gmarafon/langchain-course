import os
import requests
from dotenv import load_dotenv

load_dotenv()



def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    Scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile
    """

    if mock:
        api_endpoint = 'https://api.scrapin.io/enrichment/profile'
        params = {
            'apikey' : os.environ['SCRAPIN_API_KEY'],
            'linkedInUrl' : linkedin_profile_url
        }

        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10
        )
        
    else:
        linkedin_profile_url = 'https://gist.github.com/gmarafon/9c337b53c1210b70b7dd487462dacee3'
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
        
    
    data = response.json().get('person')
    
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ['certifications']
    }

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url= 'https://www.linkedin.com/in/eden-marco/',
            mock = True
        )
    )
