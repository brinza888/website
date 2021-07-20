import datetime

from app import db

from app.billing import p2p


class Account (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("billing_account", uselist=False), uselist=False)

    @classmethod
    def create(cls, user):
        return cls(user=user)


class Bill (db.Model):
    id = db.Column(db.String(100), primary_key=True)
    amount = db.Column(db.Integer)
    url = db.Column(db.String(255))
    creation = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.String(25), default="unknown")

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    account = db.relationship("Account", backref=db.backref("bills", lazy="dynamic"), lazy=True)

    @classmethod
    def create(cls, id, amount, url, account, creation, status):
        creation = datetime.datetime.fromisoformat(creation)
        return cls(id=id, amount=amount, url=url, account=account, creation=creation, status=status)

    def check(self):
        resp = p2p.check(self.id)
        print(resp.status)
        if self.status != resp.status:
            self.status = resp.status
            if self.status == "PAID":
                self.account.amount += self.amount
        db.session.commit()
        return self.status
