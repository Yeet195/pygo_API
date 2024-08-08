import unittest
from unittest.mock import patch, Mock
from pygo_API import Card  # Adjust the import based on your actual module name

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
            "ygoprodeck_url": "https://ygoprodeck.com/card/kuriboh-3456",
            "card_sets": [
                # Card sets data
            ],
            "card_images": [
                {"id": 40640057, "image_url": "https://images.ygoprodeck.com/images/cards/40640057.jpg", "image_url_small": "https://images.ygoprodeck.com/images/cards_small/40640057.jpg", "image_url_cropped": "https://images.ygoprodeck.com/images/cards_cropped/40640057.jpg"},
                # Additional image data
            ],
            "card_prices": [
                {"cardmarket_price": "0.11", "tcgplayer_price": "0.14", "ebay_price": "49.99", "amazon_price": "1.45", "coolstuffinc_price": "0.25"}
            ]
        }
    ]
}

class TestCard(unittest.TestCase):

    @patch('pygo_API.Cache')
    @patch('pygo_API.requests.get')
    def test_init_with_parameters(self, mock_get, mock_cache):
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response
        mock_get.return_value = mock_response
        mock_cache.get.return_value = None

        card = Card(type='Effect Monster', name='Kuriboh')

        self.assertEqual(card.data, sample_api_response)

    @patch('pygo_API.Cache')
    @patch('pygo_API.requests.get')
    def test_getData_with_fields(self, mock_get, mock_cache):
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response
        mock_get.return_value = mock_response
        mock_cache.get.return_value = None

        card = Card(type='Effect Monster', name='Kuriboh')
        result = card.getData(fields=['name', 'id'])

        self.assertEqual(result, [{'name': 'Kuriboh', 'id': 40640057}])

    @patch('pygo_API.Cache')
    @patch('pygo_API.requests.get')
    def test_getData_without_fields(self, mock_get, mock_cache):
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response
        mock_get.return_value = mock_response
        mock_cache.get.return_value = None

        card = Card(type='Effect Monster', name='Kuriboh')
        result = card.getData()

        self.assertEqual(result, sample_api_response['data'])

    @patch('pygo_API.Cache')
    @patch('pygo_API.requests.get')
    def test_random_with_fields(self, mock_get, mock_cache):
        # Mock API response for random card
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response['data'][0]
        mock_get.return_value = mock_response
        mock_cache.get.return_value = None

        card = Card()
        result = card.random(fields=['name', 'id'])

        self.assertEqual(result, {'name': 'Kuriboh', 'id': 40640057})

    @patch('pygo_API.Cache')
    @patch('pygo_API.requests.get')
    def test_random_without_fields(self, mock_get, mock_cache):
        # Mock API response for random card
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_api_response['data'][0]
        mock_get.return_value = mock_response
        mock_cache.get.return_value = None

        card = Card()
        result = card.random()

        self.assertEqual(result, sample_api_response['data'][0])

if __name__ == '__main__':
    unittest.main()
