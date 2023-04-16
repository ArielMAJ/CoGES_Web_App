from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ges_data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()


class Expenses(db.Model):
    id_exp = db.Column(db.Integer, primary_key=True, nullable=False)
    type_exp = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float(2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return "type_exp: %s, date: %s, description: %s, amount: %s" % (
            self.type_exp,
            self.date,
            self.description,
            self.amount,
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/adicionar/", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        type_exp = request.form.get("type_exp")
        date = request.form.get("date")
        if date is not None:
            date = datetime.strptime(date, "%d/%m/%Y")
        description = request.form.get("description")
        amount = request.form.get("amount")
        new_expense = Expenses(
            type_exp=type_exp, amount=amount, description=description, date=date
        )
        db.session.add(new_expense)
        db.session.commit()
        return render_template("add_expense.html", show_pop_up=True)
    return render_template("add_expense.html", show_pop_up=False)


@app.route("/tabela/", methods=["GET"])
@app.route("/tabela/<id_exp>", methods=["POST"])
def tabela(id_exp=None):
    print(id_exp, request.method)
    if request.method == "POST":
        expense = Expenses.query.filter_by(id_exp=id_exp).first()
        db.session.delete(expense)
        db.session.commit()
    expenses = sorted(Expenses.query.all(), key=lambda x: x.date, reverse=True)
    return render_template("tabela.html", expenses=expenses)


if __name__ == "__main__":
    app.run(debug=True)
