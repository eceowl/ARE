import random


class Recommender:
    def __init__(self, weather_service, eventbrite_service, netflix_service):
        self.weather_service = weather_service
        self.eventbrite_service = eventbrite_service
        self.netflix_service = netflix_service

    def get_recommendation(self, latitude, longitude):
        current_temp = self.weather_service.get_current_temperature(latitude, longitude)

        if current_temp < 60:
            print("It's cold out, here's a show to watch on netflix")

            shows = self.netflix_service.get_netflix_shows()
            # TODO Create actual recommendation algorithm
            show = random.choice(shows)

            print(self.netflix_service.get_show_information(show))
        else:
            print("It's beautiful out, get outside and do something!")
            print("Here are some free events in your area tonight!")

            print(self.eventbrite_service.get_events_around(latitude, longitude))
