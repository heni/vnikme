#!/usr/bin/python3
# coding: utf-8


import urllib.request
from lxml import etree
import datetime
import json


def extract_tag(parent, tag_name, count):
    for tag in parent:
        if tag.tag == tag_name:
            if count == 0:
                return tag
            count -= 1
    return None


def parse_date(dt):
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    dt = dt.split()
    day = int(dt[0])
    month = months[dt[1]]
    year = int(dt[2])
    return datetime.date(year, month, day)


def parse_solution(tr):
    result = {}
    for td in tr:
        cls = td.get('class', '')
        if cls == 'date':
            dt = extract_tag(td, 'nobr', 1)
            result['date'] = dt.text
        elif cls == 'problem':
            a = extract_tag(td, 'a', 0)
            result['problem'] = a.text
        elif cls == 'coder':
            a = extract_tag(td, 'a', 0)
            result['coder'] = a.text
    return result


def iterate_solutions(author, count):
    response = urllib.request.urlopen("https://acm.timus.ru/status.aspx?author={author}&status=accepted&count={count}".format(author=author, count=count))
    parser = etree.HTMLParser()
    root = etree.fromstring(response.read(), parser)
    body = extract_tag(root, 'body', 0)
    table = extract_tag(body, 'table', 0)
    tr = extract_tag(table, 'tr', 2)
    td = extract_tag(tr, 'td', 0)
    table = extract_tag(td, 'table', 0)
    for tr in table:
        if tr.attrib.get('class', '') not in ('even', 'odd'):
            continue
        solution = parse_solution(tr)
        solution['code'] = author
        if parse_date(solution['date']) < datetime.date(2020, 10, 9):
            continue
        yield solution


def main():
    authors = ['13373', '21172', '167456', '279193', '301886', '310000']
    result = {}
    data = []
    problems = {}
    for author in authors:
        data += list(iterate_solutions(author, 1000))
    for solution in data[::-1]:
        code, coder = solution['code'], solution['coder']
        if code not in result:
            result[code] = {'dates': {}, 'count': 0, 'name': coder}
            problems[code] = set()
        if solution['problem'] in problems[code]:
            continue
        problems[code].add(solution['problem'])
        coder = result[code]
        dt = parse_date(solution['date']).isoformat()
        if dt not in coder['dates']:
            coder['dates'][dt] = []
        coder['dates'][dt].append(solution['problem'])
        coder['count'] += 1
    print(json.dumps(result))


if __name__ == '__main__':
    main()

