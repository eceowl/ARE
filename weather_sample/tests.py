import unittest
from unittest.mock import MagicMock
from weather_sample.services import WeatherService, NetflixRouletteService, EventbriteService
from weather_sample.recommender import Recommender


class TestRecommender(unittest.TestCase):
    def test_bad_temperature(self):
        TEST_LATITUDE = 30
        TEST_LONGITUDE = -70

        mocked_weather_data = {
            "data": [
                {
                    "apparentTemperature": 30,
                    "precipProbability": 0
                },
                {
                    "apparentTemperature": 40,
                    "precipProbability": 0
                },
                {
                    "apparentTemperature": 50,
                    "precipProbability": 0
                }
            ]
        }

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        recommender = Recommender(weather_mock,
                                  EventbriteService(),
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(TEST_LATITUDE, TEST_LONGITUDE)
        self.assertEqual(recommendation.recommendation_type, "Netflix")

    def test_bad_precipitation(self):
        TEST_LATITUDE = 30
        TEST_LONGITUDE = -70

        mocked_weather_data = {
            "data": [
                {
                    "apparentTemperature": 75,
                    "precipProbability": 1
                },
                {
                    "apparentTemperature": 75,
                    "precipProbability": 1
                },
                {
                    "apparentTemperature": 75,
                    "precipProbability": 1
                }
            ]
        }

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        recommender = Recommender(weather_mock,
                                  EventbriteService(),
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(TEST_LATITUDE, TEST_LONGITUDE)
        self.assertEqual(recommendation.recommendation_type, "Netflix")

    def test_good_temperature(self):
        TEST_LATITUDE = 30
        TEST_LONGITUDE = -70

        mocked_weather_data = {
            "data": [
                {
                    "apparentTemperature": 80,
                    "precipProbability": .4
                },
                {
                    "apparentTemperature": 80,
                    "precipProbability": .4
                },
                {
                    "apparentTemperature": 80,
                    "precipProbability": .4
                }
            ]
        }

        mocked_event_data = [
            {
                "name": {
                    "text": "Test"
                },
                "description": {
                    "text": "This is a test"
                },
                "url": "http://www.testing.com",
            }
        ]

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        # Will still return a netflix recommendation if there are no Events in the area
        eventbrite_mock = EventbriteService()
        eventbrite_mock.get_events_around = MagicMock(return_value=mocked_event_data)

        recommender = Recommender(weather_mock,
                                  eventbrite_mock,
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(TEST_LATITUDE, TEST_LONGITUDE)
        print(recommendation)
        self.assertEqual(recommendation.recommendation_type, "Eventbrite")
