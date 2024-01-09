from backend_request.schemas import Note


def format_notes(notes: list[Note]):
    note_lines = [f"{position}: {note.title}" for position, note in enumerate(notes, 1)]
    return "\n".join(note_lines) or "Не найдено"


def format_tags(tags: str) -> list[str]:
    return tags.replace(" ", "").split(",")
