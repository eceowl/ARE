# WeatherSample

A simple "What should I do tonight?" recommendation engine based on the hourly forecast

### Build Requirements

* Register for following APIs
  * DarkSkies Weather API
    * (https://developer.forecast.io/)
  * GuideBox Entertainment API
    * (https://api.guidebox.com/)
  * Eventbrite API
    * (http://developer.eventbrite.com/)
* Create credentials.py in /weather_sample directory as follows:

class Credentials:
  api_keys = {
      "Eventbrite": "FILL_ME_IN",
      "GuideBox": "FILL_ME_IN",
      "DarkSkies": "FILL_ME_IN"
  }

