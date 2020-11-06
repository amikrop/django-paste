import paste


project = 'django-paste'

copyright = '2020, Aristotelis Mikropoulos'

author = 'Aristotelis Mikropoulos'

release = paste.__version__

version = release.rsplit('.', 1)[0]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'


def setup(app):
    app.add_object_type(
        'confval', 'confval', objname='configuration value',
        indextemplate='pair: %s; configuration value')
