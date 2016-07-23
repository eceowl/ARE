class Recommendation:
    def __init__(self, choices):
        self.choices = choices


class Choice:
    def __init__(self, title, description, url, recommendation_type, reason):
        self.reason = reason
        self.title = title
        self.description = description
        self.url = url
        self.recommendation_type = recommendation_type


class Reason:
    def __init__(self, is_stay_in_weather, reason):
        self.is_stay_in_weather = is_stay_in_weather
        self.reason = reason
