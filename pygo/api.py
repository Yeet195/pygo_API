import requests
from .cache import Cache
from .common import BASEURL, TYPEPARAMS, RACEPARAMS, LANGUAGEPARAMS, IMGURL

class APILookUp:
    '''
    A class to interact with an API to look up card data based on various parameters.
    
    Attributes:
        BASEURL (str): The base URL for the API endpoint.
        name (str, optional): The name of the card to look up.
        fname (str, optional): The full name of the card to look up.
        url (str): The constructed URL for the API request.
        data (dict): The card data retrieved from the API or cache.
    
    Methods:
        getData(): Returns the card data from the API response.
    '''
    
    BASEURL = BASEURL

    def __init__(
        self, 
        name=None, 
        type=None, 
        race=None, 
        language=None, 
        archetype=None, 
        level=None, 
        attribute=None, 
        banlist=None, 
        cardset=None, 
        fname=None, 
        _format=None, 
        linkmarker=None, 
        misc=None, 
        staple=None, 
        startdate=None, 
        enddate=None
    ):
        '''
        Initializes the APILookUp instance with the provided parameters and constructs
        the URL for the API request.

        '''
        
        self.name = name
        self.fname = fname
        self.url = f"{self.BASEURL}"
        
        # Dictionary to manage optional parameters
        params: str = {
            'type': type,
            'race': race,
            'language': language,
            'archetype': archetype,
            'level': level,
            'attribute': attribute,
            'banlist': banlist,
            'cardset': cardset,
            'fname': fname,
            'format': _format,
            'linkmarker': linkmarker,
            'misc': misc,
            'staple': staple,
            'startdate': startdate,
            'enddate': enddate
        }
        
        # Construct the URL based on parameters
        if self.name:
            self.url = f"{self.url}?name={self.name}" 
        elif self.fname:
            self.url = f"{self.url}?fname={self.fname}" 
        else:
            self.url = f"{self.url}?"
        
        for key, value in params.items():
            if value is not None:
                if key in ['type', 'race', 'language']:
                    valid_values = {
                        'type': TYPEPARAMS,
                        'race': RACEPARAMS,
                        'language': LANGUAGEPARAMS
                    }
                    if value not in valid_values[key]:
                        raise ValueError(f"Invalid {key} parameter: {value}")
                self.url += f"&{key}={value}"
        
        # Check cache first
        cached_data = Cache.get(self.url)
        if cached_data:
            self.data = cached_data
        else:
            self.response = requests.get(self.url)
            self.data = self.response.json()
            Cache.set(self.url, self.data)

    def getData(self):
        '''
        Retrieves the card data from the API response.
        
        Returns:
            dict: The card data extracted from the API response.
        '''
        return self.data["data"]

   
class APIImageLookUp:
    '''
    A class to fetch and cache images of cards based on their name and image type.
    
    Methods:
        getImage(): Retrieves the image of the card from the API or cache.
    '''
    
    BASEURL = BASEURL
    IMGURL = IMGURL

    def __init__(self, IMGTYPE, name):
        '''
        Initializes the APIImageLookUp instance with the specified image type and card name,
        and retrieves the card ID from the API.
        
        Raises:
            ValueError: If the API request fails or the card is not found.
        '''
        self.IMGTYPE: str = IMGTYPE
        self.name: str = name
        self.id = None
        self.IMGsuffix = None

        if self.IMGTYPE == "normal":
            self.IMGsuffix = "cards"
        elif self.IMGTYPE == "small":
            self.IMGsuffix = "cards_small"
        elif self.IMGTYPE == "cropped":
            self.IMGsuffix = "cards_cropped"
        else:
            self.IMGsuffix = "cards"

        # Construct the URL for fetching card data
        self.url = f"{self.BASEURL}?name={name}"
        cached_data = Cache.get(self.url)
        if cached_data:
            data = cached_data
        else:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = response.json()
                Cache.set(self.url, data)
            else:
                raise ValueError(f"API request failed with status code {response.status_code}")

        # Retrieve card ID based on name
        if 'data' in data:
            for item in data['data']:
                if item['name'].lower() == name.lower():
                    self.id = item['id']
                    break

        if self.id is None:
            raise ValueError(f"Card with name '{name}' not found.")

    def getImage(self):
        '''
        Retrieves the image of the card from the API or cache.

        Returns:
            bytes: The image data of the card.
        
        Raises:
            ValueError: If the image cannot be fetched or the card ID is not found.
        '''
        if self.id:
            image_url = f"{self.IMGURL}/{self.IMGsuffix}/{self.id}.jpg"
            cached_image = Cache.get(image_url)
            if cached_image:
                return cached_image
            else:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    Cache.set(image_url, image_data)
                    return image_data
                else:
                    raise ValueError("Image could not be fetched.")
        else:
            raise ValueError("ID not found. Cannot fetch image.")
