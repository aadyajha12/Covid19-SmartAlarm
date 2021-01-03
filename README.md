# Covid19-SmartAlarm
A Smart Flask Covid-19 alarm which comes with the latest news about Covid-19 and the weather updates.

# Requirements
User must install or have a Python version greater than 3.6, i.e - 3.7 and above

# Getting Started
The user must install certain modules for this program to be functioning properly

pip3 install flask
pip3 install uk_covid19
pip3 install requests
pip3 install sched
pip3 install threading
pip3 install logging
pip3 install pyttsx3
pip3 install pylint
pip3 install pytest

Since the API keys are unique to everyone,these keys should not be shared with anyone, thus the user must obtain his/her own News and Weather API keys from accessing https://newsapi.org and https://openweathermap.org/api respectively.

These keys should be added to config.json file which is published in this project under the news_api_key and weather_api_key
Furthermore, the default location for the weather is Exeter as stated in the json file but if the user wants to change it, he/she can enter the city name of their choice and use it :))

The server should be running locally at port 5000 as stated in the config.json file

# Handling/ Running program
Run python main.py in the main directory. The default link which the user can type to their preferred browser(suggested is Google Chrome for best performance) would be http://127.0.0.1:5000/index

According to the user's preference, they can schedule and remove alarms, notifications and choose whether to see weather or news updates.

# Author
Name :Aadya Jha
License : MIT
Github: https://github.com/aadyajha12
Email: aj534@exeter.ac.uk
