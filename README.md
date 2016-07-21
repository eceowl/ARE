# Activity Recommendation Engine

A simple "What should I do tonight?" recommendation engine based on the hourly forecast

Using the supplied Latitude and Longitude, the hourly weather is retrieved using the Dark Sky Forecast API.

### Cases

* If any upcoming hour has >70% chance of rain OR the temperature is greater than 95 degrees Fahrenheit OR less than 30 degrees Fahrenheit
    * A Netflix show will be recommended
* If these conditions aren't met then a free event located on Eventbrite will be recommended (Now < event_time < End of Day Today)
    * If there are no free events in the appropriate timespan (i.e. it's 11:30pm on a Sunday) a Netflix show will be recommended instead


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



### Rooms for Improvement
 
* Create more fine grained recommendations
    * Create a recommendation per time span (i.e. if it won't rain until 7:30 pm, make an outdoor recommendation for the hours preceding)
* Better use weather for predictions
    * 95 degrees Fahrenheit might not feel as hot depending on the humidity, etc
* Add UI to enter latitude and longitude
    