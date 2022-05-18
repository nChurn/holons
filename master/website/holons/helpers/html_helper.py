from io import StringIO
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    """Clears html from the string"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


def strip_tags(html: str) -> str:
    """Call MLStripper to strip html from the string"""
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def sanitize_str(html: str) -> str:
    html = strip_tags(html)
    html = html.strip()\
                .replace('&amp;', ' ')\
                .replace('&', ' ')\
                .replace('\t', '')\
                .replace('     ', ' ')\
                .lower()
    return html


def sanitize_talent_description(description: str) -> str:
    """Remove Upwork  description meta, leave only Skills
    """

    str_start = description.find('<b>Skills')
    str_end = description.find('<b>Country')
    skills = description[str_start-1:str_end]
    trim_1 = description.find('<b>Posted On')
    description = description[0:trim_1]
    trim_2 = description.find('<b>Hourly Range')
    description = description[0:trim_2]
    trim_3 = description.find('<b>Budget:')
    description = description[0:trim_3]
    description = description.replace(skills, '')
    return description + skills
