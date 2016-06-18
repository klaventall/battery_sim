from flask import Flask, render_template, Blueprint
import json
import pandas as pd
from pandas_highcharts.core import serialize
from pandas.compat import StringIO

myapp = Blueprint("myapp", __name__)


def create_app(debug=True):
    app = Flask(__name__)
    app.debug = debug
    app.register_blueprint(myapp, url_prefix="/myapp")
    return app

@myapp.route("/hello")
@myapp.route("/hello/<name>")
def hello(name=None):
    return render_template('hello.html', name=name)

@myapp.route('/basic')
def basic(chartID = 'poopchart', chart_type = 'bar', chart_height = 350):
    config = {
    "chart" : {"renderTo": chartID, "type": chart_type, "height": chart_height,},
    "series" : [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}],
    "title" : {"text": 'My Title'},
    "xAxis" : {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']},
    "yAxis" : {"title": {"text": 'yAxis Label'}}
    }
    return render_template('basic.html', chartID=chartID, config=json.dumps(config))


@myapp.route("/pandas")
def pandas_plot(chartID='chart_id'):
    dat = """ts;A;B;C
    2015-01-01 00:00:00;27451873;29956800;113
    2015-01-01 01:00:00;20259882;17906600;76
    2015-01-01 02:00:00;11592256;12311600;48
    2015-01-01 03:00:00;11795562;11750100;50
    2015-01-01 04:00:00;9396718;10203900;43
    2015-01-01 05:00:00;14902826;14341100;53"""
    df = pd.read_csv(StringIO(dat), sep=';', index_col='ts', parse_dates='ts')

    # Basic line plot
    chart = serialize(df, render_to="my-chart", title="FARTS", output_type='json', kind="bar")
    return render_template('my-chart.html', chart_id="my-chart", data=chart)


@myapp.route('/')
@myapp.route('/index')
def index():
    return render_template('dashboard.html')




