from flask import Flask
from data import db_session


app = Flask(__name__)


def main():
    db_session.global_init("db/ph.db")
    app.run(host="127.0.0.1", port=4000)


if __name__ == '__main__':
    main()
