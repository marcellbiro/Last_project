import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import dropbox

cities = {}

def scrape(url_key):
    URL = URLS[url_key]
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find(id='tbody')
    tds = body.find_all('td')

    counter = 0
    years = []
    i = 0
    months = []
    avg_tmp = []
    max_tmp = []
    min_tmp = []
    rainy_days = []
    rain_qty = []
    sunny_hours = []
    windy_days = []

    while counter < len(tds):
        try:
            current_td = float(tds[counter].text.replace(",", "."))
        except:
            current_td = tds[counter].text.replace(",", ".")

        if len(str(current_td)) == 0:
            counter += 1

        if i % 9 == 0:  # évek
            if len(str(current_td)) > 4:
                years += 12 * [current_td]
                counter += 1
            i = 1
        elif i % 9 == 1:  # hónapok
            months.append(current_td)
            i += 1
            counter += 1
        elif i % 9 == 2:  # középhőmérséklet
            avg_tmp.append(current_td)
            i += 1
            counter += 1
        elif i % 9 == 3:  # maximumhőmérséklet
            max_tmp.append(current_td)
            i += 1
            counter += 1
        elif i % 9 == 4:  # minimumhőmérséklet
            min_tmp.append(current_td)
            i += 1
            counter += 1
        elif i % 9 == 5:  # csapadékosnapok
            rainy_days.append(current_td)
            i += 1
            counter += 1
        elif i % 9 == 6:  # lehullott csapadék(mm)
            rain_qty.append(current_td)
            i += 1
            counter += 1
        elif i % 9 == 7:  # napsütésesórák száma
            sunny_hours.append(current_td)
            i += 1
            counter += 1
        elif i % 9 == 8:  # szelesnapok száma
            windy_days.append(current_td)
            i += 1
            counter += 1

    list_of_columns = [
        years,
        months,
        avg_tmp,
        max_tmp,
        min_tmp,
        rainy_days,
        rain_qty,
        sunny_hours,
        windy_days
    ]

    smallest_updated_variable = 1000
    for i in list_of_columns:
        if smallest_updated_variable > len(i):
            smallest_updated_variable = len(i)

    for i in range(len(list_of_columns)):
        if smallest_updated_variable < len(list_of_columns[i]):
            list_of_columns[i].pop(len(list_of_columns[i]) - smallest_updated_variable)

    town_dataframe = pd.DataFrame()
    town_dataframe["Years"] = years
    town_dataframe["Months"] = months
    town_dataframe["Average temperature"] = avg_tmp
    town_dataframe["Max temaperature"] = max_tmp
    town_dataframe["Minimum temperature"] = min_tmp
    town_dataframe["Rainy days"] = rainy_days
    town_dataframe["Rain quantity"] = rain_qty
    town_dataframe["sunny hours"] = sunny_hours
    town_dataframe["Windy days"] = windy_days

    cities[url_key] = town_dataframe


URLS = {
    "Budapest": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met001.html',
    "Győr": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met009.html',
    "Debrecen": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met002.html',
    "Kecskemét": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met003.html',
    "Kékestető": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met010.html',
    "Miskolc": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met004.html',
    "Nyíregyháza": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met011.html',
    "Pécs": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met006.html',
    "Siófok": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met007.html',
    "Szeged": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met008.html',
    "Szombathely": 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met012.html'
}

for i in URLS:
    scrape(i)

token = os.environ["USELESS_WEATHER_PASTCAST_KEY"]
dbx = dropbox.Dropbox(token)

with open('cities.pkl', 'wb') as f:
    pickle.dump(cities, f, protocol=pickle.HIGHEST_PROTOCOL)

with open("cities.pkl", "rb") as fp:
    dbx.files_upload(fp.read(), "/cities.pkl", mode=dropbox.files.WriteMode("overwrite"))
