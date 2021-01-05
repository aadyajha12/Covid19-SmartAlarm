from uk_covid19 import Cov19API
import datetime
import json
import config

def covid_uk():
# This would ensure that the data of COVID cases are only from England
    england_only = [
        'areaType=nation',
        'areaName=England'
    ]
    cases_and_deaths = {
        "date":"date",
        "areaName":"areaName",
        "areaCode":"areaCode",
        "newCasesByPublishDate":"newCasesByPublishDate",
        "cumCasesByPublishDate":"cumCasesByPublishDate",
        "newDeathsByDeathDate":'newDeathsByDeathDate',
        "cumDeathsByDeathDate":'cumDeathsByDeathDate'
    }
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    data = api.get_json()['data'][0:90]  # Returns a dictionary

    return((json.dumps(data,indent=3)))

if __name__ == "__main__":
    print(covid_uk())