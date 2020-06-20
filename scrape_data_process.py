import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met001.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

body = soup.find(id='tbody')

tds = body.find_all('td')

budapest = pd.DataFrame()

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

months.pop(-1)
avg_tmp.pop(-1)
max_tmp.pop(-1)
min_tmp.pop(-1)
rainy_days.pop(-1)


budapest["Years"] = years
budapest["Months"] = months
budapest["Average temperature"] = avg_tmp
budapest["Max temaperature"] = max_tmp
budapest["Minimum temperature"] = min_tmp
budapest["Rainy days"] = rainy_days
budapest["Rain quantity"] = rain_qty
budapest["Sunny hours"] = sunny_hours
budapest["Windy days"] = windy_days
budapest[:-4]



URL = 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met002.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

body = soup.find(id='tbody')

tds = body.find_all('td')

debrecen = pd.DataFrame()

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

months.pop(-1)
avg_tmp.pop(-1)
max_tmp.pop(-1)
min_tmp.pop(-1)
rainy_days.pop(-1)

debrecen["Years"] = years
debrecen["Months"] = months
debrecen["Average temperature"] = avg_tmp
debrecen["Max temaperature"] = max_tmp
debrecen["Minimum temperature"] = min_tmp
debrecen["Rainy days"] = rainy_days
debrecen["Rain quantity"] = rain_qty
debrecen["Sunny hours"] = sunny_hours
debrecen["Windy days"] = windy_days
debrecen[:-4]



URL = 'http://www.ksh.hu/docs/hun/xstadat/xstadat_evkozi/e_met009.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

body = soup.find(id='tbody')

tds = body.find_all('td')

gyor = pd.DataFrame()

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

months.pop(-1)
avg_tmp.pop(-1)
max_tmp.pop(-1)
min_tmp.pop(-1)
rainy_days.pop(-1)


gyor["Years"] = years
gyor["Months"] = months
gyor["Average temperature"] = avg_tmp
gyor["Max temaperature"] = max_tmp
gyor["Minimum temperature"] = min_tmp
gyor["Rainy days"] = rainy_days
gyor["Rain quantity"] = rain_qty
gyor["Sunny hours"] = sunny_hours
gyor["Windy days"] = windy_days
gyor[:-4]

cities = {
    "Győr": gyor,
    "Debrecen": debrecen,
    "Budapest": budapest
}