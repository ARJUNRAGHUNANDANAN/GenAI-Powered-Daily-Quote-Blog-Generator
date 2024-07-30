AUTHOR = 'redacted-add-your-name'
SITENAME = 'website name'
SITEURL = "" # add-final-url-here-if any-else -leave alone

PATH = "content"
STATIC_PATHS = ['content/media']

TIMEZONE = 'Europe/Rome'
THEME = "/home/{username}/Dev/Pelican/Gemini-Blog/.venv/lib/python3.12/site-packages/pelican/themes/notmyidea" #replace with username
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Home Page", "../"),
    ("Project Saadhna", "https://rsvp.withgoogle.com/events/ps-2"),
    #("Jinja2", "https://palletsprojects.com/p/jinja/"),
    #("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    #("You can add links in your config file", "#"),
    #("Another social link", "#"),
)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True