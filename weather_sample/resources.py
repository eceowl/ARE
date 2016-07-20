class Recommendation:

    def __init__(self, title, description, url, type):
        self.title = title
        self.description = description
        self.url = url
        self.type = type

    def serialize(self):
        return {
            "Title": self.title,
            "Description": self.description,
            "Url": self.url,
            "Type": self.type
        }
