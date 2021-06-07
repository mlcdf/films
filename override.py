#!/usr/bin/env python3
# Override the data passed in stdin.
# Outputs to stdout.

from typing import List, Dict

import json
import sys

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

        if ("Drame" in entry["genres"] and "Thriller" in entry["genres"]) or (
            "Biopic" in entry["genres"] and "Drame" in entry["genres"]
        ):
            entry["genres"] = [genre for genre in entry["genres"] if genre != "Drame"]

        if "Action" in entry["genres"] and "Aventure" in entry["genres"]:
            entry["genres"] = [genre for genre in entry["genres"] if genre != "Action"]

        if "Politique" in entry["genres"] and "Société" in entry["genres"]:
            entry["genres"] = ["Documentaire"]

    return collection


def main():
    data = json.load(sys.stdin)

    try:
        with open("OVERRIDE_FILE", "r") as fd:
            override = json.load(fd)
            if not isinstance(list, override):
                raise Exception(f"{OVERRIDE_FILE} should contains a list of dict.")
    except (FileNotFoundError):
        override = []

    result = merge_collection(clean_genres(data["entries"]), override)

    try:
        print(json.dumps(result, ensure_ascii=False), flush=True)
    except (BrokenPipeError, IOError):
        pass


if __name__ == "__main__":
    main()
