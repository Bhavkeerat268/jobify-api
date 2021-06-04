import uvicorn
from fastapi import FastAPI
import json
import difflib
from Recommender import Recommend
from pydantic import BaseModel
import pandas as pd
from difflib import SequenceMatcher, get_close_matches
from fastapi_pagination import Page, add_pagination, paginate
import pyrebase

app = FastAPI()
firebaseConfig = {
    "apiKey": "AIzaSyDYftrLjRC_l1xz0PoN7Exzw2NIqO27jTA",
    "authDomain": "jobifi-6e1d1.firebaseapp.com",
    "databaseURL": "https://jobifi-6e1d1-default-rtdb.firebaseio.com",
    "projectId": "jobifi-6e1d1",
    "storageBucket": "jobifi-6e1d1.appspot.com",
    "messagingSenderId": "925759922851",
    "appId": "1:925759922851:web:8cfa6e8963743c69071516",
    "measurementId": "G-0XB1EM1YTE"
}


class User(BaseModel):
    Id: str
    JobProvideName: str
    JobName: str
    JobLocation: str
    JobProvNumber:str
    Book:str


class Keyword(BaseModel):
    ckeyword: str


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()








@app.get('/')
def index():
    return {"text": "Hel ir"}


@app.post('/rec/')
def rec(keywords: Keyword):
    input_str=keywords.ckeyword
    final = Recommend.recommend(input_str)
    if len(final)==0:
        return {"recommend":"No data"}
    rec_list = []
    for x in range(len(final)):
        rec_row = {
            "id": final[x]['ID'],
            "jobprovidename": final[x]['JOBPROVIDENAME'],
            "jobname": final[x]['JOBNAME'],
            "joblocation": final[x]['JOBLOCATION'],
            "jobprovnumber": final[x]['JOBPROVNUMBER'],
            "book":final[x]['BOOK']

        }
        rec_list.append(rec_row)
    final_list = json.dumps(rec_list, default=np_encoder)

    return {"recommend": final_list}


@app.get('/rec/{idi}')
def getdetails(idi: str):
    df = pd.DataFrame()
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    jobs = db.child("JobList").get()
    if(jobs.val()==None):
        return {"item":"No data"}
    for job in jobs.each():
        df = df.append(job.val(), ignore_index=True, verify_integrity=False, sort=False)
    df.columns = df.columns.str.upper()
    mylist = df.loc[df['ID'] == idi].to_dict('records')
    print("Hello")
    print(mylist[0])
    if(len(mylist[0])==0):
         return {"item_data": "Not Found"}
    else:
        datarow = {

            "id": mylist[0]['ID'],
            "shift": mylist[0]['SHIFT'],
            "pay": mylist[0]['JOBPAY'],
            "time": mylist[0]['JOBTIMINGS'],
            "age": mylist[0]['AGESLOT'],
            "gender": mylist[0]['JOBGENDER'],
            "number": mylist[0]['JOBPROVNUMBER'],
            "book": mylist[0]['BOOK']
        }
        json_data = json.dumps(datarow, indent=4)
        return {"item_data": json_data}



@app.get('/users', response_model=Page[User])
async def get_users():
    df = pd.DataFrame()
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    jobs = db.child("JobList").get()
    if type(jobs.val()==None) and len(jobs.val())==0:
        print("True")
        users = []
        model=User(Id="None",JobProvideName="None",JobName="None",JobLocation="None",JobProvNumber="None",Book="None")
        users.append(model)
        return paginate(users)
    else:
        for job in jobs.each():
            df = df.append(job.val(), ignore_index=True, verify_integrity=False, sort=False)
        df.columns = df.columns.str.upper()
        allDatalist = df.to_dict('records')

        users = []
        for i in range(len(allDatalist)):
            model = User(Id=allDatalist[i]['ID'], JobProvideName=allDatalist[i]['JOBPROVIDENAME'],
                         JobName=allDatalist[i]['JOBNAME'],
                         JobLocation=allDatalist[i]['JOBLOCATION'], JobProvNumber=allDatalist[i]['JOBPROVNUMBER'],
                         Book=allDatalist[i]['BOOK'])
            users.append(model)

        return paginate(users)



add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
