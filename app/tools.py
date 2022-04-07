from datetime import datetime

from app.navbar import navbar


def get_year():
    return datetime.now().year


def get_datetime(f="%d.%m.%Y %H:%M"):
    return datetime.now().strftime(f)


def utility_processor():
    return dict(get_year=get_year, get_datetime=get_datetime)


def navbar_processor():
    return dict(navbar=navbar.build())


def get_shell_context_processor(**kwargs):
    def shell_context():
        return dict(kwargs)
    return shell_context
