from yozuch.view import view

# Base settings
TITLE = 'Blog title'
URL = 'http://localhost:8000'
DESCRIPTION = 'Blog description'
AUTHOR = 'Name LastName'

THEME_NAME = 'foundation'
THEME_CONFIG = {
    'disqus_shortname': None,     # example
    'google_analytics_id': None,  # UA-xxxxxxxx-x
    'github_profile_url': None,   # https://github.com/example
    'twitter_profile_url': None,  # https://twitter.com/akrylysov
    'navigation': [
        ('Blog', 'blog-index'),
        ('Tags', 'tags-index'),
        ('Archive', 'archive-index'),
        ('About', '/about/'),
        ('Feed', 'atom-feed'),
    ],
    'logo_url': '/',
}

VIEWS = (
    view('/', 'blog-index'),
    view('/blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/', 'posts'),
    view('/tags/', 'tags-index'),
    view('/tag/{slug}/', 'tags'),
    view('/archive/', 'archive-index'),
    view('/{slug}/', 'documents'),
    view('/atom.xml', 'atom-feed'),
    view('/{filename}', 'assets'),
)
