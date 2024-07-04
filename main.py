from flask import Flask, render_template, request
from flask import abort
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from summary import summarize
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
from pytube import YouTube
from deep_translator import GoogleTranslator
import requests
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import socket


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///historyq.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class History(db.Model):
   sno=db.Column(db.Integer,primary_key=True)
   title_H=db.Column(db.String(200))
   ip=db.Column(db.String(25))
   url_link= db.Column (db.String(200))
class DataStore():
  key1 = ''
  key2 = ''
  er = ''
  ur = ''
  tar=''


data = DataStore()


@app.route('/', methods=['GET', 'POST'])
def index():
  data.key1 = ''
  data.key2 = ''
  data.er = ''
  data.ur = ''
  data.tar=''
  return render_template('index.html')


@app.route('/loading', methods=['GET', 'POST'])
def loading():
  if request.method == 'POST':
    data.ur = request.form['video_url']
    data.tar=request.form['language']
    video_url = data.ur
    #
    #for transcript
    try:
      video_id = extract.video_id(video_url)
      req = requests.get(video_url)
    except:
      abort(404)
  return render_template('loading.html')


@app.route('/process_url')
def process_url():
  print("helloadfa")
  text = 'not linlting5'
  if 1 > 0:
    video_url = data.ur
    #
    #for transcript
    try:
      video_id = extract.video_id(video_url)
      req = requests.get(video_url)
    except:
      abort(404)

    if ("Video unavailable" in req.text):
      data.er = "Video unavailable"
      # return redirect(url_for('error'))
      abort(404)
    yt = YouTube(video_url)
    data.key2 = yt.title
    try:
      srt = YouTubeTranscriptApi.get_transcript(video_id)
      print("hle")
    except:
      transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
      for x, tr in enumerate(transcript_list):
        srt = YouTubeTranscriptApi.get_transcript(video_id,
                                                  languages=[tr.language_code])

      print("del")
    print(video_id)

    # print(srt)

    transcript = ''
    translimit = ''
    transcript2=''
    
    # print("\n helll")

    for value in srt:
      for key, val in value.items():
        if key == 'text':
          if (len(translimit) <= 1000):
            translimit += val
            translimit += ". "
            
          else:
            print("hllooeee")
            translated = GoogleTranslator(source='auto',
                                          target='en').translate(translimit)
            if data.tar == "Hindi":
              translated2 = GoogleTranslator(source='auto', target='hi').translate(translimit)
            else:
              translated2=translated
            print(translated)
            transcript += translated
            transcript2 += translated2

            transcript += " "
            transcript2+=" "
            translimit = ''

    if (len(translimit) > 1):
      translated = GoogleTranslator(source='auto',
                                    target='en').translate(translimit)
      if data.tar == "Hindi":
              translated2 = GoogleTranslator(source='auto', target='hi').translate(translimit)

      else:
              translated2=translated

      transcript2+=translated2
      transcript += translated
      transcript += " "
    
    lin = transcript.splitlines()
    final_tra = ".".join(lin)
    lin2 = transcript2.splitlines()
    final_tra2 = ".".join(lin2)
    print("what is ")
#START SUMMARIZATION
    print("Strat summary")
    text = final_tra
    with open("./static/css/original.txt", 'w', encoding='utf-8') as file:
        file.write(final_tra2)
    print(text)
    # return render_template('view.html', text=text)
  # Extract video ID from video_url using urlparse or other methods
  data.key1=summarize(text,.25)

  if data.tar=="Hindi":
    lines=data.key1.split(". ")
    transcript=""
    data.key1=""
    for i in lines:
        transcript+=i
        if(len(transcript)>1100):
          data.key1+=GoogleTranslator(source='auto', target='hi').translate(transcript)
          transcript=""
    data.key1+=GoogleTranslator(source='auto', target='hi').translate(transcript)
  print("this is you summay")
  print(data.key1)
  with open("./static/css/yraudio.txt", 'w', encoding='utf-8') as file:
        file.write(data.key1)
  # data.key1=summary
  return "done"


# @app.route('/error')
# def error():
#   return render_template('error.html',error="db['error']")
@app.errorhandler(404)
def page_not_found(e):
  # note that we set the 404 status explicitly
  return render_template('error.html', error=data.er, errors=e), 404


@app.route("/results")
def results():  # Finally, use the user data in some intensive process
  yt = YouTube(data.ur)
  hostname=socket.gethostname()
  ipadd=socket.gethostbyname(hostname)
  history=History(url_link=data.ur,ip=ipadd,title_H=yt.title)
  db.create_all()
  db.session.add(history)
  db.session.commit()
  def pri():
    print("###################################")
    allt=History.query.all()
    for todo in allt:
      print(todo.title_H,todo.url_link)
      print(allt)
  pri()
  return render_template('view.html', text=data.key1, tit=data.key2)


if __name__ == '__main__':
  app.run(debug=True)
