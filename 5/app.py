from dataclasses import replace
from flask import Flask, render_template,request
import os.path
import nltk
import re
from nltk.stem.snowball import SnowballStemmer

app = Flask(__name__)
nltk.download('punkt')
engStopWordsLoc="./stopwords-english.txt"
spanStopWordsLoc = "./stopwords-spanish.txt"
with open(engStopWordsLoc,'r') as f1:
    engStopWords=f1.readlines()
    engStopWords= [i.strip() for i in engStopWords]

with open(spanStopWordsLoc,'r') as f1:
    spanStopWordsLoc=f1.readlines()
    spanStopWordsLoc= [i.strip() for i in spanStopWordsLoc]

stemmer = SnowballStemmer(language='english')

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/addnew')
def addnew():
   return render_template('newfile.html')

@app.route('/search')
def search():
   return render_template('search.html')


@app.route('/addnewfileform',methods = ['POST', 'GET'])
def addnewfileform():
   fname = request.form['filename']
   fcontent = request.form['filecontent']
   msg=""
   if os.path.isfile("files/"+fname+".txt"):
      msg = "FILE "+fname+" ALREADY EXSISTS"
      return render_template('newfile.html',msg=msg)
   
   if(fname.strip()!="" and fcontent.strip()!=""):
      name="files/"+fname+".txt"
      fv =open(name,"w+")
      fv.write(fcontent)
      fv.close()
      f = open("files/filelist.txt", "a")
      f.write(fname+".txt\n")
      f.close()
      msg="FILE "+fname+" CREATED SUCCESSFULLY"
   else:
      msg="PLEASE ENTER VALID FILE NAME AND FILE CONTENT"
   return render_template('newfile.html',msg=msg)

@app.route('/searchform',methods = ['POST', 'GET'])
def searchform():
   searchtxt = request.form['searchtext']
   searchTxtList = searchtxt.split(" ")
   for i in range(len(searchTxtList)):
      searchTxtList[i] =  stemmer.stem(searchTxtList[i])
   lst=[]
   if searchtxt.strip()!="":
      msg = "SEARCH RESULTS FOR "+searchtxt
      f = open("files/filelist.txt","r")
      filelist = f.readlines()
      f.close()
      filelist = [x.strip() for x in filelist]
      for file in filelist:
         with open("files/"+file,"r",errors='ignore') as f:
            lines = f.readlines()
            for i in range(len(lines)):
               lines[i]=lines[i].strip()
               lines[i] = re.sub(r"http\S+", "", lines[i])
               lines[i] = re.sub(r'[^\w\,]+', ' ', lines[i])
               #lines[i]=re.sub('[^A-Za-z]+', ' ', lines[i])
               tokens = nltk.word_tokenize(lines[i])
               tokens=[x.lower() for x in tokens]
               stemmedWords = [stemmer.stem(x) for x in tokens]
               filteredWords=[]
               for word in stemmedWords:
                  if word not in engStopWords and word not in spanStopWordsLoc:
                     filteredWords.append(word)
               lines[i]=filteredWords

            with open("files/"+file, 'r',errors='ignore') as f1:
               originalfile = f1.readlines()
            
            l1=[]
            lineNumber = []
            for x,line in enumerate(lines):
                  for i in line:
                     for j in searchTxtList:
                        if i == j.lower() and x not in lineNumber:
                           lineNumber.append(x)
                           final = originalfile[x]
                           final = final.replace("Â", "")
                           final = final.replace("â€™", "'")
                           final = final.replace("â€œ", '"')
                           final = final.replace('â€“', '-')
                           final = final.replace('â€', '"')
                           l1.append(final.strip())
            if len(l1)>0:
               lst.append([file,l1])
      print(lst)
   else:
      msg="PLEASE ENTER VALID SEARCH TEXT"
  
   return render_template('search.html',msg=msg,lst=lst)

   
if __name__ == '__main__':
    app.run()
        