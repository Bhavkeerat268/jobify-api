import uvicorn
from fastapi import FastAPI
import json
import difflib
from Recommender import Recommend
from pydantic import BaseModel
import numpy as np
import pandas as pd
from difflib import SequenceMatcher, get_close_matches


class Keyword(BaseModel):
    ckeyword: str


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


app = FastAPI()


@app.get('/')
def index():
    return {"text": "Hel ir"}


@app.post('/rec/')
def rec(keywords: Keyword):
    input_str = keywords.ckeyword
    final = Recommend.recommend(input_str)
    rec_list = []
    for x in range(len(final)):
        rec_row = {
            "name": final[x]['NAME'],
            "job": final[x]['JOB'],
            "location": final[x]['CITY'],
            "shift": final[x]['SHIFT'],
            "pay": final[x]['SALARY'],
            "time": final[x]['TIME'],
            "age": final[x]['AGE'],
            "gender": final[x]['GENDER'],
            "id": final[x]['RANK']
        }
        rec_list.append(rec_row)
    final_list = json.dumps(rec_list, default=np_encoder)

    return {"recommend": final_list}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

