
# Client ID (Consumer Key)
# dj0yJmk9YXhyT1duanRXYjJpJmQ9WVdrOWIzUnNSREZLTXpRbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1iMA--
# Client Secret (Consumer Secret)
# 9dcf31ae4a2c45bdf5ba26656a7af833c146b4f6

import urllib2, urllib, json
images_url = "https://www.yahoo.com/sy/os/weather/1.0.1/shadow_icon/60x60/"
baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = "select * from weather.forecast where woeid in" \
            " (select woeid from geo.places(1) where text='torun, pl') and u='c'"
yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
result = urllib2.urlopen(yql_url).read()
data = json.loads(result)
# print json.dumps(data['query']['results'], indent=2)

month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul',
              8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

days_dict = {'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday', 'Mon': 'Monday',
             'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday'}

images_dict = {"Partly Cloudy": "partly_cloudy_day@2x.png", "Scattered Showers": "scattered_showers_day_night@2x.png",
               "Mostly Cloudy": "mostly_cloudy_day_night@2x.png", "Scattered Thunderstorms": "", "Thunderstorms": ""}

date_raw = data['query']['results']['channel']['lastBuildDate']

dates = date_raw.split(', ', 1)[1]

day =  dates.split(' ')[0]
month = month_dict.keys()[month_dict.values().index(dates.split(' ')[1])]
year = dates.split(' ')[2]
hour = dates.split(' ')[3]
am_pm = dates.split(' ')[4]

print "{} / {} {} {} {}".format(day, month, year, hour, am_pm)
print days_dict.values()[days_dict.keys().index(date_raw.split(', ', 1)[0])]


print data['query']['results']['channel']['item']['condition']['temp']
print data['query']['results']['channel']['item']['forecast'][0]['low']
print data['query']['results']['channel']['item']['forecast'][0]['high']
print images_url + images_dict.values()[images_dict.keys().index(data['query']['results']['channel']['item']['condition']['text'])]
