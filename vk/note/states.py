from vkbottle import BaseStateGroup
from vkbottle.dispatch.dispenser import BuiltinStateDispenser

state_dispenser = BuiltinStateDispenser()


class AddNoteStates(BaseStateGroup):
    STARTED = "STARTED"
    TITLE = "TITLE"
    BODY = "BODY"
    TAGS = "TAGS"
