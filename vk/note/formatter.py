from typing import Any


def format_notes(notes: list[dict[str, Any]]):
    notes = ["записка"]
    result = "\n".join([note for note in notes])
    return result


def format_tags(tags: str) -> list[str]:
    return tags.replace(" ", "").split(",")
