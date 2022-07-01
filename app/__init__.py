from email.policy import default
import os
from flask import Flask, render_template, make_response, request
from dotenv import load_dotenv
import re

# db imports
from peewee import *
import datetime

# model to dict
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)


# testing
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared",uri=True)
else:
    # db
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
           user=os.getenv("MYSQL_USER"),
           password=os.getenv("MYSQL_PASSWORD"),
           host=os.getenv("MYSQL_HOST"),
           port=3306
          )

print(mydb)

class TimelinePost(Model):
       name = CharField()
       email = CharField()
       content = TextField()
       created_at = DateTimeField(default=datetime.datetime.now)

       class Meta:
              database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

from .fellow_nav import fellow_nav

app.register_blueprint(fellow_nav, url_prefix='/')

# nav
nav = [{'name': 'Home', 'url': '/'},
           {'name': 'Kristen', 'url': '/kristen'},
           {'name': 'Helen', 'url': '/helen'},
           {'name': 'Catherine', 'url': '/catherine'}]


@app.route('/')
def home():
    work_info =  [{
            'name': 'Business Anaylst',
            'location': 'Scotiabank',
            'start_date': 'May 2022',
            'end_date': 'Present',
            'desc': 'Works with key stakeholders to align technology solutions with business strategies'
        },{
            'name': 'Production Engineering Fellow',
            'location': 'MLH',
            'start_date': 'May 2022',
            'end_date': 'Present',
            'desc': 'Production Engineering Fellowship hosted by MLH and Meta'
        },{
            'name': 'Software Engineer',
            'location': 'Scotiabank',
            'start_date': 'Sept 2021',
            'end_date': 'Dec 2021',
            'desc': 'Created regression models using Python and SQL to help price International ETFs'
        }]

    education_info = [{
            'name': 'University of Waterloo',
            'location': 'Waterloo, ON',
            'start_date': 'Sept 2020',
            'end_date': 'Present',
            'desc' : 'Bachelor of Computer Science Co-op'
        },{
            'name': 'Iroquois Ridge High School',
            'location': 'Oakville, ON',
            'start_date': 'Sept 2016',
            'end_date': 'June 2020',
            'desc' : 'Debate Club Marketing Executive, Interact Club Marketing Executive'
        }]

       
    hobby_info = [{
        'name' : 'Photography',
        'img' : '../static/img/helenhob1.png',
        'desc' : 'I like photographing my friends and people! I often like to adjust the picture through editing softwares. \
         the image above is a screenshot from my photography Instagram account (@hxlens).'
    },
    {
        'name' : 'Drawing',
        'img' : '../static/img/helenhob2.png',
        'desc' : 'I like drawing with different mediums. Like in forms of digitial art, paint, pencil and more.'
    }]

    return render_template('helen_page.html', nav=nav, title="Helen Xia", url=os.getenv("URL"),hobbies=hobby_info, work_info=work_info, education_info=education_info)

@app.route('/hobbies')
def helenhobbies():
    hobby_info = [{
        'name' : 'Photography',
        'img' : '../static/img/helenhob1.png',
        'desc' : 'I like photographing my friends and people! I often like to adjust the picture through editing softwares. \
         the image above is a screenshot from my photography Instagram account (@hxlens).'
    },
    {
        'name' : 'Drawing',
        'img' : '../static/img/helenhob2.png',
        'desc' : 'I like drawing with different mediums. Like in forms of digitial art, paint, pencil and more.'
    }]

    return render_template('helen_hobbies.html', nav=nav, title="Helen Xia", url=os.getenv("URL"),hobbies=hobby_info)


# timeline post
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
       print(request.form)
       try: 
           name = request.form['name'] 
       except: 
           return "Invalid name", 400
        
       # email regex
       email_re=re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-za-z0-9-]+(\.[A-Z|a-z]{2,})+')
       if re.fullmatch(email_re, request.form['email']):
               email = request.form['email'] 
       else:
               return "Invalid email", 400
       
       if (len(request.form['content']) is not 0):  
           content = request.form['content'] 
       else: 
           return "Invalid content", 400
       
       timeline_post = TimelinePost.create(name=name, email=email, content=content)
       return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
       return {
              'timeline_posts': [
                     model_to_dict(p)
                     for p in 
                     TimelinePost.select().order_by(TimelinePost.created_at.desc())
              ]
       }

@app.route('/api/timeline_post/<int:id>', methods=['DELETE'])
def delete_time_line_post():
       id = request.form['id']

       TimelinePost.delete_by_id(id)

@app.route('/timeline')
def timeline():
       posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
       return render_template('timeline.html', title="Timeline", posts=posts)
