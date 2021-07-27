from datetime import datetime

from app import db


class Release (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(20))
    description = db.Column(db.Text)
    file = db.relationship('File', uselist=False)
    date = db.Column(db.DateTime, default=datetime.now())

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))

    def __init__(self, version, description, file):
        self.version = version
        self.description = description
        self.file = file

    @property
    def released_date(self):
        return self.date.strftime("%d.%m.%Y")


class Project (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    github = db.Column(db.String(1000), nullable=True)
    started = db.Column(db.DateTime, default=datetime.now())

    releases = db.relationship(Release, lazy='dynamic', backref='project')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @property
    def started_date(self):
        return self.started.strftime("%d.%m.%Y")
