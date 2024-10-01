"""
Class for Genshin Characters
Every character will have name and birthday assigned
"""


class GenshinCharacter:

    def __init__(self, name: str, birthday: str):
        self.name = name
        self.birthday = birthday
        # Also field for image?
