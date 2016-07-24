import random, copy
from recommendation.resources import Recommendation, Reason, Choice
from datetime import datetime


class Recommender:
    def __init__(self, weather_service, eventbrite_service, netflix_service):
        self.weather_service = weather_service
        self.eventbrite_service = eventbrite_service
        self.netflix_service = netflix_service

    @staticmethod
    def __is_stay_in_weather__(weather_by_hour, timezone):
        hour = weather_by_hour['time']
        time = datetime.fromtimestamp(int(hour), timezone)
        # Prioritize rain over hot weather
        if weather_by_hour['precipProbability'] > .7:
            return Reason(time, True, "There's a good chance it might rain!")
        if weather_by_hour['temperature'] < 30:
            return Reason(time, True, "It's far too cold outside!")
        if weather_by_hour['temperature'] > 95:
            return Reason(time, True, "Whoa! It's really hot out there!")

        return Reason(time, False, "Its beautiful outside!")

    def __get_netflix_choice__(self, start_hour, end_hour, reason):
        shows = self.netflix_service.get_netflix_shows()

        # TODO actually create a recommendations algorithm for shows
        show = random.choice(shows)

        info = self.netflix_service.get_show_information(show)

        choice = Choice(
            start_hour,
            end_hour,
            info['title'],
            info['overview'],
            info['url'],
            "Netflix",
            reason
        )

        return choice

    def __get_eventbrite_choice__(self, start_hour, end_hour, latitude, longitude, reason):
        events = self.eventbrite_service.get_events_around(latitude, longitude)

        if len(events) == 0:
            overriden_reason = Reason(start_hour, True,
                                      "It's beautiful outside, but unfortunately there's nothing to do")
            return self.__get_netflix_choice__(start_hour, end_hour, overriden_reason)

        # TODO actually create a recommendations algorithm for events
        event = random.choice(events)

        choice = Choice(
            start_hour,
            end_hour,
            event['name']['text'],
            event['description']['text'],
            event['url'],
            "Eventbrite",
            reason
        )

        return choice

    def __group_weather_types__(self, hourly_weather, timezone):

        grouped_weather = []

        current_weather_group = []
        reason = self.__is_stay_in_weather__(hourly_weather[0], timezone)

        current_weather_group.append(reason)
        for hour in hourly_weather[1:]:
            reason = self.__is_stay_in_weather__(hour, timezone)

            if current_weather_group[0].reason == reason.reason:
                current_weather_group.append(reason)
            else:
                temp_group = copy.deepcopy(current_weather_group)

                grouped_weather.append(temp_group)

                current_weather_group.clear()
                current_weather_group.append(reason)

        grouped_weather.append(current_weather_group)
        return grouped_weather

    def get_recommendation(self, latitude, longitude):
        hourly_weather = self.weather_service.get_hourly_weather(latitude, longitude)
        grouped_weather = self.__group_weather_types__(hourly_weather['data'], hourly_weather['timezone'])

        choices = []
        for group in grouped_weather:
            first_item = group[0]
            last_item = group[-1]

            start_hour = first_item.hour
            end_hour = last_item.hour
            if group[0].is_stay_in_weather:
                choices.append(self.__get_netflix_choice__(start_hour, end_hour, first_item.reason))
            else:
                choices.append(
                    self.__get_eventbrite_choice__(start_hour, end_hour, latitude, longitude, first_item.reason))

        return Recommendation(choices)
