import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Query db for stocks already bought and exclude all the stocks where the sum of shares equals "0", creating a list of owned stocks
    stocks = db.execute(
        "SELECT stock, SUM(shares) AS total_shares FROM transactions WHERE id = ? GROUP BY stock HAVING total_shares != 0", session["user_id"])

    # Adds the keys and values of 'price' and 'total' to "stocks"
    for i in range(len(stocks)):
        info = lookup(stocks[i]['stock'])
        stocks[i]['price'] = info['price']
        stocks[i]['total'] = stocks[i]['price'] * stocks[i]['total_shares']

    total_sum = sum(stock['total'] for stock in stocks)
    cash_query = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash_query[0]['cash']
    total_funds = cash + total_sum

    return render_template("index.html", stocks=stocks, total_funds=total_funds, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        quoted = lookup(request.form.get("symbol"))

        # check if the symbol is valid
        if quoted == None:
            return apology("Stock symbol doesn't exist", 400)

        try:
            shares = int(request.form.get("shares"))

        # check if "shares" is a positive integer
        except ValueError:
            return apology("Invalid number of shares", 400)

        if shares <= 0:
            return apology("Invalid number of shares", 400)

        # query the db for the current cash available
        query = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = query[0]['cash']

        # calculate the total amount of funds required
        price = quoted['price']
        stock = quoted['symbol']
        balance = cash - (price * shares)
        if balance < 0:
            return apology("insufficient funds", 400)

        # Update db "transfers" and "users"
        db.execute("INSERT INTO transactions (stock, shares, price, id) VALUES (?, ?, ?, ?)",
                   stock, shares, price, session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])

        # Alert message that the purchase was successfull
        flash("Stock shares successfully bought!")

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get all transactions from user and create the column "type" to specify whether it is a "purchase" or a "sale"
    transactions = db.execute(
        "SELECT stock, shares, type, price, transacted FROM (SELECT *, CASE WHEN shares > 0 THEN 'Purchase' ELSE 'Sale' END AS type FROM transactions) WHERE id = ? ORDER BY transacted DESC", session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == 'POST':
        quoted = lookup(request.form.get("symbol"))

        # Check if symbol is valid
        if quoted == None:
            return apology("Stock symbol doesn't exist", 400)

        price = quoted['price']
        stock = quoted['symbol']
        return render_template("quoted.html", price=price, stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide valid username", 400)

        # Ensure password and validation was submitted and are the same
        elif not request.form.get("password") or not request.form.get("confirmation") or not confirmation == password:
            return apology("password provided is not valid or confirmation doesn't match", 400)

        # Generate a hash for the password
        hash = generate_password_hash(password)

        # Insert username in database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        # Ensure that there is no such username already registered
        except ValueError:
            return apology("Username already exists", 400)

        # Log in the created user
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Query db for stocks already bought and exclude all the stocks where the sum of shares equals "0", creating a list of owned stocks
    stocks = db.execute(
        "SELECT stock, SUM(shares) AS total_shares FROM transactions WHERE id = ? GROUP BY stock HAVING total_shares != 0", session["user_id"])

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Check if "shares" is a positive integer
        if shares <= 0 or not isinstance(shares, int):
            return apology("Invalid number of shares", 400)

        # Check how many shares the user owns
        owned_shares = 0
        for stock in stocks:
            if stock['stock'] == symbol:
                owned_shares = stock['total_shares']
                break

        if owned_shares == 0:
            return apology("Stock not currently owned", 400)

        # check if user owns at least the same amount of shares being sold
        elif shares > owned_shares:
            return apology("User doesn't own enough shares", 400)

        # query the db for the current cash available
        query = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = query[0]['cash']

        # calculate the value of the shares
        quoted = lookup(symbol)
        price = quoted['price']
        balance = cash + (price * shares)
        shares_sold = -shares

        # Update db "transfers" and "users"
        db.execute("INSERT INTO transactions (stock, shares, price, id) VALUES (?, ?, ?, ?)",
                   symbol, shares_sold, price, session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])

        # Alert message that the purchase was successfull
        flash("Stock shares successfully sold!")

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    query = db.execute("SELECT username, cash FROM users WHERE id = ?", session["user_id"])
    username = query[0]['username']
    cash = query[0]['cash']
    if request.method == "POST":
        # Add more cash to the logged user
        try:
            amount = float(request.form.get("add_cash"))

            # Check if amount to be add is valid
            if amount <= 0:
                return apology("Not a valid amount of money", 400)
        except ValueError:
            return apology("Not a valid amount of money", 400)

        # Sum the amount to the previously owned cash and update the db
        balance = amount + cash
        balance = round(balance, 2)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])
        flash("Cash successfully added!")
        return redirect("/profile")
    else:
        return render_template("profile.html", username=username, cash=cash)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        password = request.form.get("password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure id exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid current password and/or invalid logged user", 403)

        # Ensure password and validation was submitted and are the same
        if not request.form.get("new_password") or not request.form.get("confirmation") or not confirmation == new_password:
            return apology("new password provided is not valid and/or confirmation doesn't match", 403)

        # Generate a hash for the new password
        hash = generate_password_hash(new_password)

        # Insert new hash in database
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, session["user_id"])

        # Alert message that the operation was successful
        flash("Password successfully changed!")

        return redirect("/profile")
    else:
        return render_template("change_password.html")
