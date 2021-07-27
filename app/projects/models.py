from app import db


class Release (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(20))
    description = db.Column(db.Text)
    file = db.relationship('File', uselist=False)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))

    def __init__(self, version, description, file):
        self.version = version
        self.description = description
        self.file = file


class Project (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    github = db.Column(db.String(1000), nullable=True)

    releases = db.relationship(Release, lazy='dynamic', backref='project')

    def __init__(self, name, description):
        self.name = name
        self.description = description
