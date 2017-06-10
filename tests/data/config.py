from yozuch.view import view

DEBUG = True

RST_OPTIONS = {
    'add_heading_permalink': True,
}

THEME_NAME = 'test'
THEME_CONFIG = {
    'foo': 'bar',
}

VIEWS = (
    view('/', 'blog-index'),
    view('/paginated_index.html', 'blog-index', posts_per_page=1, pagination_url='/page/{number}/',
         template='blog_index.html'),
    view('/blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/', 'posts'),
    view('/tags/', 'tags-index'),
    view('/tag/{slug}/', 'tags'),
    view('/archive/', 'archive-index'),
    view('/atom.xml', 'atom-feed'),
    view('/{filename}', 'assets'),
    view('/url1.html', 'documents', template='template1.html', source='/documents/page.rst'),
    view('/documents/{slug}/', 'documents', template='document.html', source='/documents/page2.rst'),
    view('/documents/{slug}/', 'documents', template='document.html', source='/documents/page3.rst'),
    view('/{filename}', 'pages'),
)

FOO = 'bar'
