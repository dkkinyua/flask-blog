from flask import Flask, render_template
import datetime as dt

app = Flask(__name__)

current_time = dt.datetime.now()
formatted_datetime = current_time.strftime("%Y-%m-%d %H:%M")

posts = [
    {
        'author': 'D.Kinyua',
        'title': 'First blog post',
        'content': 'First blog post here',
        'date_posted': formatted_datetime
    },
    {
        'author': 'D.Ngige',
        'title': 'Second blog post',
        'content': 'Second blog post here',
        'date_posted': formatted_datetime
    }
]



@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')