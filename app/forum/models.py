from app import db
from app.models import User


class Theme (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Theme #{self.id} {self.title}>"


class Thread (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    theme_id = db.Column(db.Integer, db.ForeignKey("theme.id"))
    theme = db.relationship(Theme, uselist=False, backref=db.backref("threads", lazy="dynamic"))

    base_message_id = db.Column(db.Integer, db.ForeignKey("message.id"))
    base_message = db.relationship("Message", uselist=False, foreign_keys=[base_message_id])

    def __repr__(self):
        return f"<Thread '{self.title}'#{self.id} in {self.theme}>"


class Message (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    thread_id = db.Column(db.Integer, db.ForeignKey("thread.id"))
    thread = db.relationship(Thread, uselist=False, backref=db.backref("messages", lazy="dynamic"),
                             foreign_keys=[thread_id])

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(User, uselist=False, backref=db.backref("forum_messages", lazy="dynamic"))

    def __repr__(self):
        return f"<Message #{self.id} on {self.thread}>"
