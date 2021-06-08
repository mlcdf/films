#!/usr/bin/env python3

from typing import List, Dict

import argparse
import json
import logging


OVERRIDE_FILE = "override.json"


def merge_collection(main: List[Dict], override: List[Dict]):
    if len(override) == 0:
        return main

    collection: Dict[str, Dict] = {}

    for entry in main:
        id = entry.pop("id")
        collection[id] = entry

    for entry in override:
        if entry["id"] in collection:
            collection[entry["id"]].update(entry)

    return [{"id": id, **entry} for (id, entry) in collection.items()]


def clean_genres(collection: List[Dict]):
    for entry in collection:
        if entry is None or "genres" not in entry:
            continue

        if (
            ("Drame" in entry["genres"] and "Thriller" in entry["genres"])
            or ("Biopic" in entry["genres"] and "Drame" in entry["genres"])
            or ("Guerre" in entry["genres"] and "Drame" in entry["genres"])
        ):
            entry["genres"] = [genre for genre in entry["genres"] if genre != "Drame"]

        if "Action" in entry["genres"] and "Aventure" in entry["genres"]:
            entry["genres"] = [genre for genre in entry["genres"] if genre != "Action"]

        if "Gangster" in entry["genres"] and "Policier" in entry["genres"]:
            entry["genres"] = [
                genre for genre in entry["genres"] if genre != "Policier"
            ]

        if "Gangster" in entry["genres"] and "Policier" in entry["genres"]:
            entry["genres"] = [
                genre for genre in entry["genres"] if genre != "Policier"
            ]

        if "Politique" in entry["genres"] and "Société" in entry["genres"]:
            entry["genres"] = ["Documentaire"]

    return collection


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", type=argparse.FileType("r+"), help="file to override", metavar="FILE"
    )
    parser.add_argument("--in-place", "-i", action="store_true")
    args = parser.parse_args()

    data = json.load(args.file)
    args.file.close()

    try:
        with open(OVERRIDE_FILE, "r") as fd:
            override = json.load(fd)
            if not isinstance(override, list):
                raise Exception(f"{OVERRIDE_FILE} should contains a list of dict.")
    except (FileNotFoundError):
        logging.exception("not override file found")
        override = []

    data["entries"] = merge_collection(clean_genres(data["entries"]), override)

    if not args.in_place:
        try:
            print(json.dumps(data, ensure_ascii=False), flush=True)
        except (BrokenPipeError, IOError):
            pass
    else:
        with open(args.file.name, "w+") as fd:
            json.dump(data, fd, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
