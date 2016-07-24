class Recommendation:
    def __init__(self, choices):
        self.choices = choices


class Choice:
    def __init__(self, start_hour, end_hour, title, description, url,  recommendation_type, reason):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.reason = reason
        self.title = title
        self.description = description
        self.url = url
        self.recommendation_type = recommendation_type


class Reason:
    def __init__(self, hour, is_stay_in_weather, reason):
        self.hour = hour
        self.is_stay_in_weather = is_stay_in_weather
        self.reason = reason
