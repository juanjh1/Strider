import enum
import regex as re 

class RegexPattern(enum.Enum):
    PASSWORD = (r"^(?=.*\p{Ll})(?=.*\p{Lu})(?=.*[0-9])(?=.*[-.@?¡!¿])[-\p{L}0-9.@?¡!¿]{8,16}$", "Password")
    EMAIL =( r'^[\p{L}\p{Nd}_"][-\p{L}\p{Nd}_+".]+[\p{L}\p{Nd}_"](?<!\.\.)@[-\p{L}\p{Nd}]+(?:\.[\p{L}]{2,63})+$', "Email")
    USERNAME = (r'^(?!.*__)(?!.*--)(?=.*\p{l})[\p{L}][-\p{L}_\p{Nd}]{0,28}[\p{L}\p{Nd}]$', "Username")
    NAME = (r'^\p{L}{1,15}(\s+\p{L}{1,15}){0,2}$', "Name")
    LASTNAME = (r'^\p{L}{1,15}(\s+\p{L}{1,15}){0,2}$', "Last name")

    def __init__(self, pattern, field_name):
        self.__pattern = re.compile(pattern)
        self.__field_name = field_name

    def get_field_name(self):
        return self.__field_name
    def validate(self, text):
        return self.__pattern.match(text) 
    

