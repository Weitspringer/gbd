import htmlGenerator

from tatsu import exceptions
from core.main import groups, search
from core.database.db import Database


from flask import Flask, render_template, request, url_for

app = Flask(__name__)

from os.path import realpath, dirname, join

DATABASE = join(dirname(realpath(__file__)), 'local.db')


@app.route("/", methods={'GET'})
def welcome():
    return render_template('home.html')  # file is found at runtime


@app.route("/resolve/<hash>", methods=['GET'])
def resolve(hash):
    param = request.args.to_dict()
    result = ""
    with Database(DATABASE) as database:
        if len(param.keys()) == 0:
            attributes = groups.reflect(database)

        for name in param.keys():
            value = search.resolve(database, name, hash)
            result += "{} {}\n".format(name, *value)
    return result


@app.route("/test", methods=['GET'])
def test():
    return render_template('test.html')


@app.route("/query_form", methods=['GET'])
def query_form():
    return render_template('query_form.html')


@app.route("/query", methods=['POST'])   # query string über post
def query():
    response = htmlGenerator.generate_html_header("en")
    response += htmlGenerator.generate_head("Results")
    query = request.values.to_dict()["query"]
    with Database(DATABASE) as database:
        try:
            list = search.find_hashes(database, query)
        except exceptions.FailedParse:
            return "Not a valid query argument"
        response += htmlGenerator.generate_table_div(list)

    return response

