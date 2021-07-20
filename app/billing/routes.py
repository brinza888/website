from flask import *
from flask_login import login_required, current_user

from app import db
from app.billing import bp, p2p
from app.billing.models import Bill, Account


@bp.route("/")
@login_required
def account():
    if current_user.billing_account:
        account_bills = current_user.billing_account.bills.order_by(Bill.creation).all()
        return render_template("billing/account.html", account_bills=account_bills)
    return render_template("billing/account.html")


@bp.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    if not current_user.billing_account:
        return redirect(url_for("billing.account"))

    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount:
            return render_template("billing/payment.html")

        resp = p2p.bill(amount=amount, currency="RUB", comment="Пополнение баланса brinzabezrukoff.xyz")
        bill = Bill.create(resp.bill_id, resp.amount, resp.pay_url, current_user.billing_account,
                           resp.creation, resp.status)
        db.session.add(bill)
        db.session.commit()
        return redirect(resp.pay_url)
    return render_template("billing/payment.html")


@bp.route("/open_account", methods=["POST"])
@login_required
def open_account():
    acc = Account.create(current_user)
    db.session.add(acc)
    db.session.commit()
    return redirect(url_for("billing.account"))
