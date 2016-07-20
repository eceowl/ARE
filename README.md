# Activity Recommendation Engine

A simple "What should I do tonight?" recommendation engine based on the hourly forecast

### Build Requirements

* Register for following APIs
  * Dark Sky Forecast API
    * (https://developer.forecast.io/)
  * GuideBox API
    * (https://api.guidebox.com/)
  * Eventbrite API
    * (http://developer.eventbrite.com/)
* Create credentials.py in /weather_sample directory as follows:

```python
class Credentials:
  api_keys = {
      "Eventbrite": "FILL_ME_IN",
      "GuideBox": "FILL_ME_IN",
      "DarkSkies": "FILL_ME_IN"
  }
```

* Create a virtualenv and run ``pip install -r requirements.txt``
* Set the FLASK_APP by running ``export FLASK_APP=weather_sample/main.py``
* Run the command ``flask run``
* In your browser or with curl/wget hit the endpoint ``http://127.0.0.1:5000/recommendations/{LATITUDE},{LONGITUDE}``
