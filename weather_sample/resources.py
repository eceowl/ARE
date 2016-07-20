class Recommendation:

    def __init__(self, title, description, url, recommendation_type):
        self.title = title
        self.description = description
        self.url = url
        self.recommendation_type = recommendation_type

    def serialize(self):
        return {
            "Title": self.title,
            "Description": self.description,
            "Url": self.url,
            "Type": self.recommendation_type
        }
