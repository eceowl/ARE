import requests
from recommendation.credentials import Credentials
from datetime import timedelta, date, datetime, time
import pytz


class EventbriteService:
    BASE_URL = "https://www.eventbriteapi.com/v3/"
    O_AUTH = Credentials.api_keys['Eventbrite']

    def __format_request_url__(self, resource):
        return self.BASE_URL \
               + "/".join([str(r) for r in resource])

    def get_events_around(self, latitude, longitude):
        resource = ["events", "search"]
        params = {
            "location.latitude": latitude,
            "location.longitude": longitude,
            "start_date.range_start": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "start_date.range_end": (date.today() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            "price": "free",
            "include_unavailable_events": "false"
        }

        response = requests.get(
            self.__format_request_url__(resource),
            headers={
                "Authorization": "Bearer " + self.O_AUTH
            },
            verify=True,
            params=params
        )

        return response.json()['events']


class NetflixRouletteService:
    BASE_URL = "https://api-public.guidebox.com/v1.43"
    API_KEY = Credentials.api_keys['GuideBox']

    def __format_request_url__(self, params):
        return self.BASE_URL \
               + "/US" \
               + "/" + self.API_KEY + "/" \
               + "/".join([str(p) for p in params])

    def get_netflix_shows(self):
        params = ["shows", "netflix", 20, 50]
        url = self.__format_request_url__(params)

        data = requests.get(url).json()
        return data['results']

    def get_show_information(self, show):
        params = ["show", show['id']]
        url = self.__format_request_url__(params)

        data = requests.get(url).json()

        return data


class WeatherService:
    DARK_SKIES_URL = "https://api.forecast.io/forecast"
    API_KEY = Credentials.api_keys['DarkSkies']

    def __format_request_url__(self, latitude, longitude):
        return "{}/{}/{},{}".format(self.DARK_SKIES_URL,
                                    self.API_KEY,
                                    latitude,
                                    longitude)

    def get_current_weather(self, latitude, longitude):
        url = self.__format_request_url__(latitude, longitude)
        response = requests.get(url)

        data = response.json()
        return data

    def get_current_temperature(self, latitude, longitude):
        data = self.get_current_weather(latitude, longitude)
        return data['currently']['apparentTemperature']

    def get_hourly_weather(self, latitude, longitude):
        data = self.get_current_weather(latitude, longitude)

        timezone_name = data['timezone']
        timezone = pytz.timezone(timezone_name)
        print(timezone_name)

        tomorrow = datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=1)
        midnight = datetime.combine(tomorrow, time())

        # For this to be accurate, you would need to look up the timezone of the longitude and latitude provided
        # Also this is gonna round down the number of hours left in the day, but this is okay because most likely
        # There won't be any events that start at midnight anyway
        hours_left = (midnight.replace(tzinfo=timezone).astimezone(timezone) - datetime.now(timezone)).seconds // 3600
        return data['hourly']['data'][0:hours_left]
