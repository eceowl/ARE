import unittest
import pytz
import time
from unittest.mock import MagicMock
from recommendation.services import WeatherService, NetflixRouletteService, EventbriteService
from recommendation.recommender import Recommender


class TestRecommender(unittest.TestCase):
    """
        Single Recommendation Choices (i.e. weather pattern is consistent throughout the day
    """

    TEST_TIMEZONE = pytz.timezone("America/New_York")
    TEST_LATITUDE = 30
    TEST_LONGITUDE = -70

    def test_bad_temperature(self):
        mocked_weather_data = {
            "timezone": self.TEST_TIMEZONE,
            "data": [
                dict(time=time.time(), temperature=30, precipProbability=0),
                dict(time=time.time(), temperature=40, precipProbability=0),
                dict(time=time.time(), temperature=50, precipProbability=0)
            ]
        }

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        recommender = Recommender(weather_mock,
                                  EventbriteService(),
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(self.TEST_LATITUDE, self.TEST_LONGITUDE)
        self.assertEqual(len(recommendation.choices), 1)
        self.assertEqual(recommendation.choices[0].recommendation_type, "Netflix")

    def test_bad_precipitation(self):
        mocked_weather_data = {
            "timezone": self.TEST_TIMEZONE,
            "data": [
                dict(time=time.time(), temperature=75, precipProbability=1.0),
                dict(time=time.time(), temperature=75, precipProbability=1.0),
                dict(time=time.time(), temperature=75, precipProbability=1.0)
            ]
        }

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        recommender = Recommender(weather_mock,
                                  EventbriteService(),
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(self.TEST_LATITUDE, self.TEST_LONGITUDE)
        self.assertEqual(len(recommendation.choices), 1)
        self.assertEqual(recommendation.choices[0].recommendation_type, "Netflix")

    def test_good_temperature(self):
        mocked_weather_data = {
            "timezone": self.TEST_TIMEZONE,
            "data": [
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4)
            ]
        }

        mocked_event_data = [
            dict(name={
                "text": "Test"
            }, description={
                "text": "This is a test"
            }, url="http://www.testing.com")
        ]

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        # Will still return a netflix recommendations if there are no Events in the area
        eventbrite_mock = EventbriteService()
        eventbrite_mock.get_events_around = MagicMock(return_value=mocked_event_data)

        recommender = Recommender(weather_mock,
                                  eventbrite_mock,
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(self.TEST_LATITUDE, self.TEST_LONGITUDE)
        self.assertEqual(len(recommendation.choices), 1)
        self.assertEqual(recommendation.choices[0].recommendation_type, "Eventbrite")

    """
        Multiple weather pattern choices
    """

    def test_good_then_rainy(self):
        mocked_weather_data = {
            "timezone": self.TEST_TIMEZONE,
            "data": [
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.8),
                dict(time=time.time(), temperature=80, precipProbability=.8),
                dict(time=time.time(), temperature=80, precipProbability=.8)
            ]
        }

        mocked_event_data = [
            dict(name={
                "text": "Test"
            }, description={
                "text": "This is a test"
            }, url="http://www.testing.com")
        ]

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        # Will still return a netflix recommendations if there are no Events in the area
        eventbrite_mock = EventbriteService()
        eventbrite_mock.get_events_around = MagicMock(return_value=mocked_event_data)

        recommender = Recommender(weather_mock,
                                  eventbrite_mock,
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(self.TEST_LATITUDE, self.TEST_LONGITUDE)
        self.assertEqual(len(recommendation.choices), 2)
        self.assertEqual(recommendation.choices[0].recommendation_type, "Eventbrite")
        self.assertEqual(recommendation.choices[1].recommendation_type, "Netflix")
        self.assertEqual(recommendation.choices[0].reason.reason, "Its beautiful outside!")
        self.assertEqual(recommendation.choices[1].reason.reason, "There's a good chance it might rain!")

    def test_good_then_hot(self):
        mocked_weather_data = {
            "timezone": self.TEST_TIMEZONE,
            "data": [
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=100, precipProbability=.4),
                dict(time=time.time(), temperature=100, precipProbability=.4),
                dict(time=time.time(), temperature=100, precipProbability=.4)
            ]
        }

        mocked_event_data = [
            dict(name={
                "text": "Test"
            }, description={
                "text": "This is a test"
            }, url="http://www.testing.com")
        ]

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        # Will still return a netflix recommendations if there are no Events in the area
        eventbrite_mock = EventbriteService()
        eventbrite_mock.get_events_around = MagicMock(return_value=mocked_event_data)

        recommender = Recommender(weather_mock,
                                  eventbrite_mock,
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(self.TEST_LATITUDE, self.TEST_LONGITUDE)
        self.assertEqual(len(recommendation.choices), 2)
        self.assertEqual(recommendation.choices[0].recommendation_type, "Eventbrite")
        self.assertEqual(recommendation.choices[1].recommendation_type, "Netflix")
        self.assertEqual(recommendation.choices[0].reason.reason, "Its beautiful outside!")
        self.assertEqual(recommendation.choices[1].reason.reason, "Whoa! It's really hot out there!")

    def test_hot_then_good(self):
        mocked_weather_data = {
            "timezone": self.TEST_TIMEZONE,
            "data": [
                dict(time=time.time(), temperature=100, precipProbability=.4),
                dict(time=time.time(), temperature=100, precipProbability=.4),
                dict(time=time.time(), temperature=100, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4),
                dict(time=time.time(), temperature=80, precipProbability=.4)
            ]
        }

        mocked_event_data = [
            dict(name={
                "text": "Test"
            }, description={
                "text": "This is a test"
            }, url="http://www.testing.com")
        ]

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        # Will still return a netflix recommendations if there are no Events in the area
        eventbrite_mock = EventbriteService()
        eventbrite_mock.get_events_around = MagicMock(return_value=mocked_event_data)

        recommender = Recommender(weather_mock,
                                  eventbrite_mock,
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(self.TEST_LATITUDE, self.TEST_LONGITUDE)
        self.assertEqual(len(recommendation.choices), 2)
        self.assertEqual(recommendation.choices[0].recommendation_type, "Netflix")
        self.assertEqual(recommendation.choices[1].recommendation_type, "Eventbrite")
        self.assertEqual(recommendation.choices[0].reason.reason, "Whoa! It's really hot out there!")
        self.assertEqual(recommendation.choices[1].reason.reason, "Its beautiful outside!")

    def test_rainy_then_good(self):
        mocked_weather_data = {
            "timezone": self.TEST_TIMEZONE,
            "data":
                [
                    dict(time=time.time(), temperature=70, precipProbability=1),
                    dict(time=time.time(), temperature=70, precipProbability=1),
                    dict(time=time.time(), temperature=70, precipProbability=1),
                    dict(time=time.time(), temperature=70, precipProbability=.4),
                    dict(time=time.time(), temperature=70, precipProbability=.4),
                    dict(time=time.time(), temperature=70, precipProbability=.4)
                ]
        }

        mocked_event_data = [
            dict(name={
                "text": "Test"
            }, description={
                "text": "This is a test"
            }, url="http://www.testing.com")
        ]

        weather_mock = WeatherService()
        weather_mock.get_hourly_weather = MagicMock(return_value=mocked_weather_data)

        # Will still return a netflix recommendations if there are no Events in the area
        eventbrite_mock = EventbriteService()
        eventbrite_mock.get_events_around = MagicMock(return_value=mocked_event_data)

        recommender = Recommender(weather_mock,
                                  eventbrite_mock,
                                  NetflixRouletteService())

        recommendation = recommender.get_recommendation(self.TEST_LATITUDE, self.TEST_LONGITUDE)
        self.assertEqual(len(recommendation.choices), 2)
        self.assertEqual(recommendation.choices[0].recommendation_type, "Netflix")
        self.assertEqual(recommendation.choices[1].recommendation_type, "Eventbrite")
        self.assertEqual(recommendation.choices[0].reason.reason, "There's a good chance it might rain!")
        self.assertEqual(recommendation.choices[1].reason.reason, "Its beautiful outside!")
