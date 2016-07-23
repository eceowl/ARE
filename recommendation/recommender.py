import random, copy
from recommendation.resources import Recommendation, Reason, Choice


class Recommender:
    def __init__(self, weather_service, eventbrite_service, netflix_service):
        self.weather_service = weather_service
        self.eventbrite_service = eventbrite_service
        self.netflix_service = netflix_service

    @staticmethod
    def __is_stay_in_weather__(weather_by_hour):
        if weather_by_hour['temperature'] < 30:
            return Reason(True, "It's far too cold outside!")
        if weather_by_hour['temperature'] > 95:
            return Reason(True, "Whoa! It's really hot out there!")
        if weather_by_hour['precipProbability'] > .7:
            return Reason(True, "There's a good chance it might rain!")

        return Reason(False, "Its beautiful outside!")

    def __get_netflix_choice__(self, reason):
        shows = self.netflix_service.get_netflix_shows()

        # TODO actually create a recommendations algorithm for shows
        show = random.choice(shows)

        info = self.netflix_service.get_show_information(show)

        choice = Choice(
            info['title'],
            info['overview'],
            info['url'],
            "Netflix",
            reason
        )

        return choice

    def __get_eventbrite_choice__(self, latitude, longitude, reason):
        events = self.eventbrite_service.get_events_around(latitude, longitude)

        if len(events) == 0:
            overriden_reason = Reason(True, "It's beautiful outside, but unfortunately there's nothing to do")
            return self.__get_netflix_choice__(overriden_reason)

        # TODO actually create a recommendations algorithm for events
        event = random.choice(events)

        choice = Choice(
            event['name']['text'],
            event['description']['text'],
            event['url'],
            "Eventbrite",
            reason
        )

        return choice

    def __group_weather_types__(self, hourly_weather):

        grouped_weather = []

        current_weather_group = []
        reason = self.__is_stay_in_weather__(hourly_weather[0])

        current_weather_group.append(reason)
        for hour in hourly_weather[1:]:
            reason = self.__is_stay_in_weather__(hour)

            if current_weather_group[0].reason == reason.reason:
                current_weather_group.append(reason)
            else:
                temp_group = copy.deepcopy(current_weather_group)

                grouped_weather.append(temp_group)

                current_weather_group.clear()
                current_weather_group.append(reason)

        grouped_weather.append(current_weather_group)
        print(grouped_weather)
        return grouped_weather

    def get_recommendation(self, latitude, longitude):
        hourly_weather = self.weather_service.get_hourly_weather(latitude, longitude)
        grouped_weather = self.__group_weather_types__(hourly_weather)

        choices = []
        for group in grouped_weather:
            group_item = group[0]
            if group[0].is_stay_in_weather:
                choices.append(self.__get_netflix_choice__(group_item.reason))
            else:
                choices.append(self.__get_eventbrite_choice__(latitude, longitude, group_item.reason))

        return Recommendation(choices)
