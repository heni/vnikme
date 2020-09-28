import json


def fetch_raw_cases_deaths(country_code):
    data = json.loads(open('/home/vnik/work/vnikme/frontend/vnikme/covid.json', 'rt').read())
    cases, deaths, tests, last_ds = [], [], [], None
    if country_code not in data:
        return cases, deaths, tests, '', last_ds
    country_data = data[country_code]
    location = country_data['location']
    for entry in country_data['data']:
        if 'date' not in entry:
            continue
        cases.append(entry.get('new_cases', 0))
        deaths.append(entry.get('new_deaths', 0))
        tests.append(entry.get('new_tests', 0))
        last_ds = entry['date']
    return cases, deaths, tests, location, last_ds


def rolling_average(data, window):
    result, sums = [], []
    s = 0.0
    for x in data:
        s += x
        sums.append(s)
    for i in range(window, len(data)):
        result.append(int((sums[i] - (sums[i - window - 1] if i > window else 0.0)) // window))
    return result

