from pathlib import PurePath


def root_path() -> PurePath:
    return PurePath(__file__).parent.parent.parent
