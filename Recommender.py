from difflib import get_close_matches
import numpy as np
import pandas as pd
import pyrebase

# df = pd.read_csv("final_dataset.csv")
# df.drop(df.columns[df.columns.str.contains('Unnamed',case = False)],axis = 1, inplace = True)
# df.isnull().any()
# df = df.replace(r'^\s+$', np.nan, regex=True)
# df = df.dropna()
# df.head(5)

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




def combine_features(row):
    return row['JOBLOCATION'] + " " + row['JOBNAME'] + " " + row['SHIFT'] + " " + row['AGESLOT'] + " " + row[
        'JOBGENDER'] + " " + row['ID']



class Recommend:
    def recommend(data):
        df = pd.DataFrame()
        empty_data=[]
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        jobs = db.child("JobList").get()
        if(jobs.val()==None):
            return empty_data
        for job in jobs.each():
            df = df.append(job.val(), ignore_index=True, verify_integrity=False, sort=False)
        print(df)
        df.columns = df.columns.str.upper()
        df["COMBINED_FEATURES"] = df.apply(combine_features, axis=1)

        recommendations = []
        match = get_close_matches(data, df["COMBINED_FEATURES"], n=20, cutoff=0.5)

        final = []
        ranklist = []


        for x in range(len(match)):
            a = match[x].split(' ')
            final.append(a)
            ranklist.append(final[x][5])

        dfu=df.loc[df['ID'].isin(ranklist)]
        print(dfu.to_dict('records'))

        return dfu.to_dict('records')









