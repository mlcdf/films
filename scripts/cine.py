import json
import os

with open(os.path.join(os.getcwd(), "content", "data", "cinema.json"), "r", encoding="utf-8") as fd:
    cinema = json.load(fd)


with open(os.path.join(os.getcwd(), "content", "data", "mlcdf", "films-done.json"), "r", encoding="utf-8") as fd:
    films = json.load(fd)

def xx(film: dict):
    id = film.pop("id")
    return film

cinema: dict["str", dict] = { cine["id"]:xx(cine) for cine in cinema["entries"] }

for film in films["entries"]:
    if film["id"] in cinema:
        film["cinema"] = True
    else:
        film["cinema"] = False

    film["revu"] = False

# with open(os.path.join(os.getcwd(), "content", "data", "journal.json"), "w", encoding="utf-8") as fd:
#     json.dump(films, fd, indent=4)