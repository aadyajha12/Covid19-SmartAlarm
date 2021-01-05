# pylint: disable=line-too-long, unsubscriptable-object, global-statement, bare-except

import time
import json
import random
import sched
import threading
import logging
from datetime import datetime
import pyttsx3
from flask import render_template
from flask import Flask
from flask import request
from newsapi import *
from weatherapi import *
from ukcovid19 import *


notifications = [] # an array for current notifications
old_notifications = [] # an array for removed notiifcations
alarms = [] # an array for the alarms

config = json.load(open('config.json')) # open the config file and load it as a dictionary
weather_api_key = config['weather_api_key'] # extract the weather api key
news_api_key = config['news_api_key'] # extract the news api key

s = sched.scheduler(time.time, time.sleep) # initialise the schedular
logging.basicConfig(filename='sys.log', level=logging.INFO) # initialise the logging module

app = Flask(__name__) # initialise the flask app
app.logger.disabled = True # disable console logging for flask
logging.getLogger('werkzeug').disabled = True # disable logging for flask in the log file
logging.getLogger('comtypes.client._code_cache').disabled = True # disable other kind of logging

try:
    CURRENT_WEATHER = extract_weather(weather_api_key, config['city_name']).json() # get the weather for current city
except:
    logging.error('%s:An error has occured with the weather API', datetime.datetime.now())

def trigger_alarm(data: dict) -> None:
    '''
    This function is used to trigger an alarm, it is only called on
    when an alarm is meant to go off
    keyword argument:
    data -- the alarm information such as content, title etc.
    '''

    logging.info('Alarm called %s is going off at %s', data['title'], datetime.datetime.now())
    engine = pyttsx3.init() # initialise the tts engine
    engine.say('Your alarm called %s is going off' % data['title']) # announce that the alarm is going off
    if data['weather']: # if the weather is enabled
        try:
            engine.say('''
            The current temperature is {0} degrees celcius. 
            The level of humidity is {1} percent. 
            And lastly, the weather is described as {2}
            '''.format(CURRENT_WEATHER['temperature'], CURRENT_WEATHER['humidity'], CURRENT_WEATHER['description'])) # announce the weather
        except:
            logging.error('%s:An error occured with the weather API', datetime.datetime.now())

    if data['news']: # if the news is enabled
        try:
            t_articles = random.sample((covid_news(news_api_key).json()), 10)
            news_content = set([a['title'] for a in t_articles])
            engine.say('Here are some top news articles: {0}'.format('. '.join(news_content))) # announce 3 random news articles
        except:
            logging.error('%s:An error occured with the news API', datetime.datetime.now())

    try:
        covid = covid_news(API_KEY) # get the covid data for england
        cases = covid['newCasesByPublishDate'] # get cases today
        deaths = covid['newDeaths28DaysByPublishDate'] # get deaths today for people who tested positive in the last 28 days
        cum_cases = covid['cumCasesByPublishDate'] # get total cases
        cum_deaths = covid['cumDeaths28DaysByPublishDate'] # get total deaths for people who tested positive in the last 28 days

        engine.say('''
        In regards, to COVID-19, there have been {0} cases and {1} deaths today.
        In total, there have bee {2} cases and {3} deaths.
        '''.format(cases, deaths, cum_cases, cum_deaths)) # announce the covid data
    except:
        logging.error('%s:An error occured with the covid API', datetime.datetime.now())


    engine.runAndWait()
    del data['alarm_object'] # delete the scheduler event from the dictionary
    alarms.remove(data) # delete the alarm from the alarms list


@app.route('/index')
def index() -> None:
    '''
    This function runs whenever a user goes to /index
    '''
    try:
        update_notifications() # update the notifications
    except:
        logging.error('%s:An error occured with updating the notifications')
    notif = request.args.get('notif') # parse the url
    alarm_item = request.args.get('alarm_item')
    alarm = request.args.get('alarm')
    news =  bool(request.args.get('news'))
    weather = bool(request.args.get('weather'))

    if notif: # if they're removing a notification
        for notification in notifications: # for each notification in the list of notifications
            if notification['title'] == notif: # if the notification matches the notification being removed
                notifications.remove(notification) # remove the notification from the list of notifications
                old_notifications.insert(0, notification) # add the notification to the list of old notifications
                logging.info('%s:"%s" was removed from the list of notifications', datetime.datetime.now(), notification['title'])

    if alarm_item: # if they're removing an alarm
        for alarm_ in alarms: # for each alarm in the list of alarms
            if alarm_['title'] == alarm_item: # if the alarm matches the alarm being removed
                alarms.remove(alarm_) # remove the alarm from the list of alarms
                s.cancel(alarm_['alarm_object']) # cancel the alarm int he scheduler
                try:
                    data = json.load(open('alarms.json')) # load the alarms.json file into a dictionary
                    del alarm_['alarm_object'] # delete the scheduler event from the dictionary
                    data.remove(alarm_) # remove the alarm from the alarms.json file
                    alarms_file = open('alarms.json', 'w') # open the alarms.json file with the ability to edit it
                    alarms_file.write(json.dumps(data, indent=4)) # save the new list of alarms to alarms.json
                except json.decoder.JSONDecodeError:
                    logging.error('%s:There was an issue updating the alarms.json file', datetime.datetime.now())

                logging.info('%s:"%s" was removed from the list of alarms',  datetime.datetime.now(), alarm_['title'])
    try:
        if alarm: # if they're setting an alarm
            alarm_date = datetime.datetime.strptime(alarm, '%Y-%m-%dT%H:%M').timestamp() # convert the date and time to a timestamp
            current_date = datetime.datetime.now().timestamp() # get the current timestamp

            if alarm_date - current_date > 0: # if the alarm is set in the future
                content = 'The alarm is set to go off at {0}.'
                if news: # if the news is going to be announced
                    content += ' The news will be announced.'

                if weather: # if the weather is going to be announced
                    content += ' The weather will be announced.'

                content = content.format(alarm.replace('T', ' '))
                alarm_data = { # save the alarm data as a dictionary
                    'alarm': alarm,
                    'title': request.args.get('two'),
                    'news': news,
                    'weather': weather,
                    'content': content
                }

                try:
                    data = json.load(open('alarms.json')) # load the alarms.json file into a dictionary
                    data.append(alarm_data) # add the alarm to the alarms.json file
                    alarms_file = open('alarms.json', 'w') # open the alarms.json file with the ability to edit it
                    alarms_file.write(json.dumps(data, indent=3)) # save the new list of alarms to alarms.json
                except json.decoder.JSONDecodeError:
                    logging.error('%s:There was an issue uploading the alarm to the alarms.json file', datetime.datetime.now())


                alarm_object = s.enter(alarm_date - current_date, 1, trigger_alarm, (alarm_data, )) # schedule the alarm
                threading.Thread(target=s.run).start() # create a new thread and run the scheduler and start the thread
                alarm_data['alarm_object'] = alarm_object # append the schedule event to the alarm dictionary
                alarms.append(alarm_data) # add the alarm to the list of alarms
                logging.info('%s:An alarm called "%s" has been set for %s', datetime.datetime.now(), alarm_data['title'], datetime.datetime.fromtimestamp(alarm_date))
            else:
                logging.warning('%s:An alarm called "%s" was set for the past, it has been cancelled', datetime.datetime.now(), request.args.get('two'))
    except ValueError:
        logging.error('%s:The user entered an invalid date', datetime.datetime.now())

    title = config['title'] # get the title for the alarm
    return render_template('index.html', title=title, image='image.png',notifications=notifications,alarms=alarms ) # render the page

def update_notifications():
    '''
    This function is used to update notifications with information
    from the news, weather and covid api
    '''

    try:
        for article in covid_news(news_api_key).json(): # for each article in the articles from the api
            if article not in notifications and article not in old_notifications: # if the notification isn't in current notifications and not in old notifications
                notifications.insert(0, {
                    'title': article['title'],
                    'content': article['content']
                }) # insert the notification in the list of notifications
                logging.info('%s:"%s" was added to the list of notifications', datetime.datetime.now(), article['title'])
    except:
        logging.error('%s:An error occured with the news API', datetime.datetime.now())

    try:
        new_weather = (extract_weather(weather_api_key, config['city']).json()) # get the weather for the current city
        global CURRENT_WEATHER # set the variable as a global variable

        if new_weather != CURRENT_WEATHER: # if the weather has changed
            content = ''
            if new_weather['temperature'] != CURRENT_WEATHER['temperature']: # if the temperature changed
                content += ' The temperature has changed from {0}°C to {1}°C.'.format(
                    str(CURRENT_WEATHER['temperature']), str(new_weather['temperature'])
                )

            if new_weather['humidity'] != CURRENT_WEATHER['humidity']: # if the humidity changed
                content += ' The level of humidity has changed from {0}% to {1}%.'.format(
                    CURRENT_WEATHER['humidity'], new_weather['humidity']
                )

            if new_weather['description'] != CURRENT_WEATHER['description']: # if the description changed
                content += ' The description of the weather has changed from {0} to {1}.'.format(
                    CURRENT_WEATHER['description'], new_weather['description']
                )

            notifications.insert(0, {
                'title': 'Weather Update - {0}'.format(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')),
                'content': content
            }) # insert the weather update to the notifications
            CURRENT_WEATHER = new_weather # update the current weather variable
            logging.info('%s:"%s" was added to the list of notifications', datetime.datetime.now(), notifications[0]['title'])
    except:
        logging.error('%s:An error occured with the weather API', datetime.datetime.now())

    try:
        covid = covid_uk() # get the covid data for england
        cases = covid['newCasesByPublishDate'] # get cases today
        deaths = covid['newDeathsyPublishDate'] # get deaths today for people who tested positive in the last 28 days
        cases_threshold = config['covid_infected_threshold'] # get the covid infected threshold from the config file
        deaths_threshold = config['covid_death_threshold'] # get the covid death threshold from the config file
        deaths = deaths if deaths else 0 # if deaths is None, set it as 0

        if cases >= cases_threshold or deaths >= deaths_threshold: # if the cases or deaths is higher than the thresholds
            covid_content = 'Thare are currently {0} new cases today, and {1} new deaths today'.format(cases, deaths)
            covid_notif = {
                'title': 'COVID Update',
                'content': covid_content
            }

            if (covid_notif not in notifications) and (covid_notif not in old_notifications): # if the notification is new
                notifications.insert(0, covid_notif) # insert the covid update to the notifications
                logging.info('%s:"%s" was added to the list of notifications', datetime.datetime.now(), covid_notif['title'])
    except:
        logging.error('%s:An error occured with the covid API', datetime.datetime.now())


def check_alarms() -> None:
    '''
    This function is used to retrieve any alarms that will go off
    in the future in the case that the program restarts/crashes
    '''

    try:
        alarms_file = open('alarms.json') # open the alarms.json file
        data = json.load(alarms_file) # load it into the dictionary

        for alarm in data: # for each alarm in the alarms file
            alarm_date = datetime.datetime.strptime(alarm['alarm'], '%Y-%m-%dT%H:%M').timestamp() # get the date/time the alarm is meant to go off
            current_date = datetime.datetime.now().timestamp() # gett he current date as a timestamp
            delay = alarm_date - current_date # get the delay
            if delay > 0: # if the alarm is going to go off in the future
                alarm_object = s.enter(delay, 1, trigger_alarm, (alarm, )) # schedule the alarm
                thread = threading.Thread(target=s.run) # create a new thread and run the scheduler
                thread.start() # start the thread
                alarm['alarm_object'] = alarm_object # append the schedule event to the alarm dictionary
                alarms.append(alarm) # add the alarm to the list of alarms
                logging.info('%s:An alarm called "%s" has been restored and set for %s', datetime.datetime.now(), alarm['title'], alarm_date)
    except json.decoder.JSONDecodeError:
        logging.error('%s:There was an issue loading the alarms from the alarms.json file', datetime.datetime.now())


if __name__ == '__main__':
    update_notifications() # update the notifications
    check_alarms() # check if there are any alarms saved that can be loaded in
    app.run(port=config['port'], debug=True) # run the flask app