import os
import itertools
import json
from datetime import datetime

import pygal

class Period:
    year: int
    month: int
    day: int

    def __init__(self, year: int, month: int  = 0, day: int  = 0) -> None:
        if day < 1 or day > 31:
            raise ValueError("day must be in 0..31")
        if month < 1 or month > 12:
            raise ValueError("month must be in 0..12")
        if year < 0 :
            raise ValueError("year must be greater than 0")

        self.year = year
        self.month = month
        self.day = day

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Period):
            raise ValueError("")

        return self.year == __o.year and self.month == __o.month and self.day == __o.day

    def __gt__(self, __o: object) -> bool:
        if not isinstance(__o, Period):
            raise ValueError("")

        if self.year > __o.year:
            return True

        if self.year == __o.year and self.month > __o.month:
            return True

        if self.year == __o.year and self.month == __o.month and self.day > __o.day:
            return True

        return False

    def __lt__(self, __o: object) -> bool:
        return self.__gt__(__o)


def parse_date(film: dict):
    if film["done_date"].endswith("-00-00"):
        film["done_date"] = datetime.strptime(film["done_date"].replace("-00", ""), "%Y")
    elif film["done_date"].endswith("-00"):
        film["done_date"] = datetime.strptime(film["done_date"].replace("-00", ""), "%Y-%m")
    else:
        film["done_date"] = datetime.strptime(film["done_date"], "%Y-%m-%d")

    return film


with open(os.path.join(os.getcwd(), "content", "data", "journal.json")) as fd:
    journal = json.load(fd)

    films = [ parse_date(film) for film in journal["entries"] if "done_date" in film]
    films = [ film for film in films if film["done_date"].year > 2013]

groups = { k: list(g) for k, g in itertools.groupby(sorted(films, key=lambda element: element["done_date"].year), key=lambda element: element["done_date"].year) }

years = [year for year, _ in groups.items()]

bar_chart = pygal.StackedBar()
# bar_chart.title = 'Films vu'
bar_chart.x_labels = map(str, years)
bar_chart.add('au cinéma', [len([f for f in films if f["cinema"] is True]) for year, films in groups.items()])
bar_chart.add('à la maison',  [len([f for f in films if f["cinema"] is False]) for year, films in groups.items()])
bar_chart.render_to_file(os.path.join(os.getcwd(), "test.svg"))

def ssum(l: list) -> list:
    out  = []
    for i, e in enumerate(l):
        out.append(sum(l[0:1+i]))
    return out

bar_chart = pygal.StackedLine(fill=True)
# bar_chart.title = 'Évolution du nombre de films vus'
bar_chart.x_labels = map(str, years)
bar_chart.add('au cinéma', ssum([len([f for f in films if f["cinema"] is True]) for year, films in groups.items()]))
bar_chart.add('à la maison',  ssum([len([f for f in films]) for year, films in groups.items()]))
bar_chart.render_to_file(os.path.join(os.getcwd(), "test2.svg"))

print("\n".join([f["title"] for f in groups[2018] if f["cinema"] is True]))
