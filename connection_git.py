import oauth2
import json
import regex
import schedule
import time
import os
import datetime


file_name = datetime.datetime.now().strftime("%Y-%m-%d") + ".json"
old_file_name = file_name

def change_name(name):
    global file_name
    file_name = name
    print file_name

def insert_row(tweets, file):
    for statuses in tweets['statuses']:
        nuevo = json.dumps(statuses, sort_keys=True, indent=4, separators=(',', ': '))
        nuevo = json.loads(nuevo)
        text = clear_date(nuevo['text'])
        location = clear_date(nuevo['user']['location'])
        time_zone = str(nuevo['user']['time_zone'])
        utc_offset = str(nuevo['user']['utc_offset'])
        name = clear_date(nuevo['user']['name'])
        screen_name = clear_date(nuevo['user']['screen_name'])
        id_user = str(nuevo['user']['id_str'])
        id_tweet = str(nuevo['id_str'])
        print id_tweet
        print id_user

        file.write(text + ',' + location + ',' + time_zone + ',' +
                   utc_offset + ',' + name + ',' + "@" + screen_name + ',' + "'" + id_user + "'" + ',' + "'" + id_tweet + "'" + '\n')

def insert_row_without_parser(tweets,file):
    contador = 0
    for statuses in tweets['statuses']:
        new_row = json.dumps(statuses, sort_keys=True, indent=4, separators=(',', ': '))
        file.write(new_row)
        contador = contador + 1
        if contador < len(tweets['statuses']):
            file.write(",\n")



def clear_date(text):
    text = str(regex.sub(u"(\u2018|\u2019)", "'", text.encode('ascii', 'ignore')))
    text = str(regex.sub(u"(\n)", "", text.encode('ascii', 'ignore')))
    text = str(regex.sub(',', "", text.encode('ascii', 'ignore')))
    return text

def authentication():
    QUERY_MENTION = "https://api.twitter.com/1.1/search/tweets.json?q=%23DonaldTrump%20OR%20OR%20%40realDonaldTrump&locale=en&count=200&src=typd"
    QUERY_MENTION_DONALD_TRUMP = "https://api.twitter.com/1.1/search/tweets.json?q=%3ArealDonaldTrump&locale=en&result_type=recent"

    QUERY_USER = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=realDonaldTrump&count=2"

   
    CONSUMER_KEY = "********"
    CONSUMER_SECRET = "********"
    ACCESS_KEY = "********"
    ACCESS_SECRET = "***********"


    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth2.Client(consumer, access_token)

    timeline_endpoint = QUERY_MENTION
    response, data = client.request(timeline_endpoint)

    return json.loads(data)

def dataBase():
    global old_file_name
    global file_name
    tweets = authentication()
    f = open("result.txt", "w+r")
    f.write(json.dumps(tweets, sort_keys=True, indent=4, separators=(',', ': ')))
    file_name = datetime.datetime.now().strftime("%Y-%m-%d") + ".json"
    print old_file_name

    if (os.path.isfile(file_name)==False):
        file = open(file_name, "w")
        file.write("[")
        if old_file_name != file_name:
           old_file = open(old_file_name,"a+r")
           old_file.write("]")
           old_file_name = file_name
    else:
        file = open(file_name, "a+r")
        file.write(",\n")
    insert_row_without_parser(tweets, file)




schedule.every(15).minutes.do(dataBase)
print "Realizado"
#schedule.every().hour.do(dataBase)
#schedule.every().day.at("10:30").do(dataBase)
while 1:
    schedule.run_pending()
    time.sleep(1)

