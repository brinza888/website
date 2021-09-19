from flask import url_for, request


class NavElement:
    def __init__(self, view, title):
        self.view = view
        self.title = title


class Navbar:
    def __init__(self, elements=None):
        self.elements = []
        elements = [] or elements
        for el in elements:
            self.add_element(*el)
    
    def add_element(self, view, title):
        self.elements.append(NavElement(view, title))

    def build(self):
        for el in self.elements:
            yield url_for(el.view), el.title, el.view == request.endpoint


navbar = Navbar([
        ('main.index', 'Главная'),
        ('projects.index', 'Мои проекты'),
        # ('main.news', 'Новости'),
        ('main.contacts', 'Контакты'),
])


def navbar_ctx_processor():
    return dict(navbar=navbar.build())
