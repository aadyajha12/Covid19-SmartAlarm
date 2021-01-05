from ukcovid19 import covid_uk

def covid_test_one():
    stats_covid = covid_uk()
    assert stats_covid['cumDeathsByPublishDate'] >= 79344

def covid_test_two():
    stats_covid = covid_uk()
    assert stats_covid['cumCasesByPublishDate'] >= 2286803

def covid_test_three():
    stats_covid = covid_uk()
    assert stats_covid['cumCasesByPublishDate'] != None