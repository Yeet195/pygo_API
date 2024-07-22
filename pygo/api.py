import requests
from cache import Cache
from common import BASEURL, TYPEPARAMS, RACEPARAMS, LANGUAGEPARAMS, IMGURL

class APILookUp:
    BASEURL = BASEURL

    def __init__(
        self, 
        name, 
        type=None, 
        race=None, 
        language=None, 
        archetype=None, 
        level=None, 
        attribute=None, 
        banlist=None, 
        cardset=None, 
        fname=None, 
        format=None, 
        linkmarker=None, 
        misc=None, 
        staple=None, 
        startdate=None, 
        enddate=None
    ):
        self.name = name
        self.url = f"{self.BASEURL}?name={name}"
        
        # Dictionary to manage optional parameters
        params = {
            'type': type,
            'race': race,
            'language': language,
            'archetype': archetype,
            'level': level,
            'attribute': attribute,
            'banlist': banlist,
            'cardset': cardset,
            'fname': fname,
            'format': format,
            'linkmarker': linkmarker,
            'misc': misc,
            'staple': staple,
            'startdate': startdate,
            'enddate': enddate
        }
        
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

    def get_data(self):
        return self.data["data"]

   
class APIImageLookUp:
    BASEURL = BASEURL
    IMGURL = IMGURL

    def __init__(self, IMGTYPE, name):
        self.IMGTYPE = IMGTYPE
        self.name = name
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

        # Check cache first
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

        if 'data' in data:
            for item in data['data']:
                if item['name'].lower() == name.lower():
                    self.id = item['id']
                    break

        if self.id is None:
            raise ValueError(f"Card with name '{name}' not found.")

    def getImage(self):
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

lookup = APIImageLookUp(
    "small",
	"7 Colored Fish"
)
content = lookup.getImage()