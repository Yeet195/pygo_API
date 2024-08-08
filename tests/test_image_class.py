import unittest
from unittest.mock import patch, Mock
from pygo_API import Image  # Adjust the import based on your actual module name

# Sample API response to be used in tests
sample_api_response = {
    "data": [
        {
            "id": 40640057,
            "name": "Kuriboh",
            "type": "Effect Monster",
            "frameType": "effect",
            "desc": "During damage calculation, if your opponent's monster attacks (Quick Effect): You can discard this card; you take no battle damage from that battle.",
            "atk": 300,
            "def": 200,
            "level": 1,
            "race": "Fiend",
            "attribute": "DARK",
            "archetype": "Kuriboh",
            "card_images": [
                {"id": 40640057, "image_url": "https://images.ygoprodeck.com/images/cards/40640057.jpg", "image_url_small": "https://images.ygoprodeck.com/images/cards_small/40640057.jpg", "image_url_cropped": "https://images.ygoprodeck.com/images/cards_cropped/40640057.jpg"}
            ]
        }
    ]
}

class TestImage(unittest.TestCase):

    @patch('pygo_API.Cache.get')
    @patch('pygo_API.Cache.set')
    @patch('pygo_API.requests.get')
    def test_init_with_name(self, mock_requests_get, mock_cache_set, mock_cache_get):
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response
        mock_requests_get.return_value = mock_response
        mock_cache_get.return_value = None

        image = Image(IMGTYPE='normal', name='Kuriboh')

        self.assertEqual(image.id, 40640057)
        self.assertEqual(image.name, 'Kuriboh')
        self.assertEqual(image.IMGsuffix, 'cards')

    @patch('pygo_API.Cache.get')
    @patch('pygo_API.Cache.set')
    @patch('pygo_API.requests.get')
    def test_getImage(self, mock_requests_get, mock_cache_set, mock_cache_get):
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'test image data'
        mock_requests_get.return_value = mock_response
        mock_cache_get.side_effect = lambda url: None if 'cards' in url else sample_api_response

        image = Image(IMGTYPE='normal', name='Kuriboh')
        result = image.getImage(size='normal')

        self.assertEqual(result, b'test image data')
        mock_requests_get.assert_called_with('https://images.ygoprodeck.com/images/cards/40640057.jpg')

    @patch('pygo_API.Cache.get')
    @patch('pygo_API.Cache.set')
    @patch('pygo_API.requests.get')
    def test_init_with_fname(self, mock_requests_get, mock_cache_set, mock_cache_get):
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response
        mock_requests_get.return_value = mock_response
        mock_cache_get.return_value = None

        image = Image(IMGTYPE='small', fname='kuriboh')

        self.assertEqual(image.id, 40640057)
        self.assertEqual(image.fname, 'kuriboh')
        self.assertEqual(image.IMGsuffix, 'cards_small')

    @patch('pygo_API.Cache.get')
    @patch('pygo_API.Cache.set')
    def test_getImage_with_cache(self, mock_cache_set, mock_cache_get):
        # Mock cache to return image data
        mock_cache_get.side_effect = lambda url: b'cached image data' if 'cards/40640057.jpg' in url else sample_api_response

        image = Image(IMGTYPE='normal', name='Kuriboh')
        result = image.getImage(size='normal')

        self.assertEqual(result, b'cached image data')

if __name__ == '__main__':
    unittest.main()
