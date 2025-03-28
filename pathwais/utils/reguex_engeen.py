import enum
import regex as re 

class ReguexPatter(enum.Enum):
    PASSWORD = r"^(?=.*\p{Ll})(?=.*\p{Lu})(?=.*[0-9])(?=.*[-.@?¡!¿])[-\p{L}0-9.@?¡!¿]{8,16}$"
    EMAIL = r'^[\p{L}\p{Nd}_"][-\p{L}\p{Nd}_+".]+[\p{L}\p{Nd}_"](?<!\.\.)@[-\p{L}\p{Nd}]+(?:\.[\p{L}]{2,63})+$'
    USERNAME = r''

    def __init__(self, pattern):
        self.pattern = pattern

    def validate(self, text):
        return bool(re.match(self.pattern, text) is not None)
    

