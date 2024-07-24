import requests
from .cache import Cache
from .common import BASEURL, TYPEPARAMS, RACEPARAMS, LANGUAGEPARAMS, IMGURL, ENDPOINTS

class Card:
    '''
    A class to interact with an API to look up card data based on various parameters.
    
    Attributes:
        BASEURL (str): The base URL for the API endpoint.
        url (str): The constructed URL for the API request.
        data (dict): The card data retrieved from the API or cache.
    
    Methods:
        getData(fields=None): Returns the card data from the API response, with optional filtering of specific keys.
        random(fields=None): Returns random card data from the API response, with optional filtering of specific keys.
    '''
    
    BASEURL = BASEURL
    RANDOMURL = "https://db.ygoprodeck.com/api/v7/randomcard.php"

    def __init__(self, **kwargs):
        '''
        Initializes the APILookUp instance with the provided parameters and constructs
        the URL for the API request.
        '''
        self.url = f"{self.BASEURL}?"
        
        # Construct the URL based on provided parameters
        for key, value in kwargs.items():
            if key in ENDPOINTS and value is not None:
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

    def getData(self, fields=None):
        '''
        Retrieves the card data from the API response with optional filtering of specific keys.
        
        Args:
            fields (list): A list of keys to include in the output. If None, returns all available data.
        
        Returns:
            dict: The card data extracted from the API response, filtered by specified keys.
        '''
        data = self.data.get("data", [])
        if fields:
            filtered_data = []
            for item in data:
                filtered_item = {key: item[key] for key in fields if key in item}
                filtered_data.append(filtered_item)
            return filtered_data
        return data
    
    def random(self, fields=None):
        '''
        Retrieves random card data from the API response with optional filtering of specific keys.
        
        Args:
            fields (list): A list of keys to include in the output. If None, returns all available data.
        
        Returns:
            dict: The random card data extracted from the API response, filtered by specified keys.
        '''
        # Check cache first
        cached_data = Cache.get(self.RANDOMURL)
        if cached_data:
            data = cached_data
        else:
            response = requests.get(self.RANDOMURL)
            data = response.json()
            Cache.set(self.RANDOMURL, data)
        
        if fields:
            filtered_data = {key: data[key] for key in fields if key in data}
            return filtered_data
        return data
        
class Image:
    '''
    A class to fetch and cache images of cards based on their name and image type.
    
    Methods:
        getImage(image_type='normal'): Retrieves the image of the card from the API or cache.
    '''
    
    BASEURL = BASEURL
    IMGURL = IMGURL

    def __init__(self, IMGTYPE, name=None, save=None, fname=None):
        '''
        Initializes the APIImageLookUp instance with the specified image type and card name,
        and retrieves the card ID from the API.
        
        Raises:
            ValueError: If the API request fails or the card is not found.
        '''
        self.save = save
        self.IMGTYPE = IMGTYPE
        self.name = name
        self.fname = fname
        self.id = None
        self.IMGsuffix = None
        
        if self.name is None and self.fname is None:
            raise ValueError("Either 'name' or 'fname' is required")

        if self.IMGTYPE == "normal":
            self.IMGsuffix = "cards"
        elif self.IMGTYPE == "small":
            self.IMGsuffix = "cards_small"
        elif self.IMGTYPE == "cropped":
            self.IMGsuffix = "cards_cropped"
        else:
            self.IMGsuffix = "cards"

        # Construct the URL for fetching card data
        if self.fname is not None:
            self.url = f"{self.BASEURL}?fname={self.fname}"
        else:
            self.url = f"{self.BASEURL}?name={self.name}"
        
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

        # Retrieve card ID based on name or fname
        if 'data' in data:
            for item in data['data']:
                card_name = item['name'].lower()
                if self.name and card_name == self.name.lower():
                    self.id = item['id']
                    break
                elif self.fname and self.fname.lower() in card_name:
                    self.id = item['id']
                    break
                       
        if self.id is None:
            raise ValueError(f"Card with name '{self.name or self.fname}' not found.")

    def getImage(self, size='normal'):
        '''
        Retrieves the image of the card from the API or cache based on the specified image size.

        Args:
            size (str): The size of the image to retrieve ('normal', 'small', 'cropped'). Defaults to 'normal'.
        
        Returns:
            bytes: The image data of the card.
        
        Raises:
            ValueError: If the image cannot be fetched or the card ID is not found.
        '''
        if self.id:
            if size == 'normal':
                image_url = f"{self.IMGURL}/cards/{self.id}.jpg"
            elif size == 'small':
                image_url = f"{self.IMGURL}/cards_small/{self.id}.jpg"
            elif size == 'cropped':
                image_url = f"{self.IMGURL}/cards_cropped/{self.id}.jpg"
            else:
                raise ValueError("Invalid image size. Choose from 'normal', 'small', 'cropped'.")

            cached_image = Cache.get(image_url)
            if cached_image:
                return cached_image
            else:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content
                    Cache.set(image_url, image_data)
                    if self.save:
                        with open(f"{self.name or self.fname}.jpg", 'wb') as f:
                            f.write(image_data)
                    return image_data
                else:
                    raise ValueError("Image could not be fetched.")
        else:
            raise ValueError("ID not found. Cannot fetch image.")
