from flask import Flask, render_template, request, send_file
from teamdata import teamdata
from graph import grapf
import base64
from io import BytesIO
import io
import base64
import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns
import pickle


app = Flask(__name__)

@app.route("ipl-win-predict-dataanalysis.herokuapp.com/stats")
def visualize():
    df= pd.read_csv('IPL Matches 2008-2020.csv' ,index_col=False)
    fig,ax = plt.subplots(figsize=(20,10))
    sns.countplot(y='toss_winner', data=df, order=df['winner'].value_counts().index)
    plt.ylabel('toss_winner',fontsize=12)
    plt.xlabel('No: of matches',fontsize=12)
    plt.title('Number of toss winning team',fontsize=12)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot_url1 = base64.b64encode(buf.getbuffer()).decode("ascii")

    fig,ax = plt.subplots(figsize=(20,10))
    sns.countplot(y='winner', data=df, order=df['winner'].value_counts().index)
    plt.xlabel('No: of Wins',fontsize=12)
    plt.ylabel('Team',fontsize=12)
    plt.title('Matches won by the Teams ', fontsize=12)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot_url2 = base64.b64encode(buf.getbuffer()).decode("ascii")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.countplot(y='player_of_match', data=df, order=df['player_of_match'].value_counts().iloc[:10].index,
                  palette='rainbow')
    plt.xlabel('No: of matches', fontsize=12)
    plt.title('Most man of Match', fontsize=16)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot_url3 = base64.b64encode(buf.getbuffer()).decode("ascii")

    fig, ax = plt.subplots(figsize=(20, 10))
    sns.countplot(y='venue', hue='toss_decision', data=df,
                  order=df['venue'].value_counts().iloc[:10].index.sort_values(), palette='deep')
    plt.ylabel('venue', fontsize=12)
    plt.xlabel('Count', fontsize=12)
    plt.title('Decision to field or bat in each venue', fontsize=16)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot_url4 = base64.b64encode(buf.getbuffer()).decode("ascii")

    fig, ax = plt.subplots(figsize=(20, 10))
    toss_data = {"Matches_won_by_toss_winner": 418,
                 "Matches_won_by_toss_looser": 398}
    toss_data = pd.Series(toss_data)
    plt.pie(x=toss_data, autopct="%.2f%%", labels=toss_data.index);
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plot_url5 = base64.b64encode(buf.getbuffer()).decode("ascii")

    return render_template('chat.html',plot_url1=plot_url1 , plot_url2=plot_url2,plot_url3=plot_url3,plot_url4=plot_url4,plot_url5=plot_url5)

@app.route("/")
def header():
    return render_template("homepage.html")

@app.route("ipl-win-predict-dataanalysis.herokuapp.com/team",methods=['GET'])
def team():
    if request.method == 'GET':
        teamNameSarch=request.args['teamName']
        top5_Batsman,top5_Bowler=teamdata(teamNameSarch).load_data()
        return render_template('team.html',top5_Batsman=top5_Batsman,top5_Bowler=top5_Bowler,teamNameSarch=teamNameSarch)

@app.route("/prediction",methods=['GET'])
def prediction():
    if request.method == 'GET':
        return render_template('winPrediction.html')

@app.route("/result",methods=['GET'])
def result():
    if request.method == 'GET':
        batting_team = request.args['batting']
        bowling_team = request.args['bowling']
        city = request.args['city']
        Target = request.args['Target']
        Score = request.args['Score']
        Overs_completed = request.args['Overs completed']
        Wickets_out = request.args['Wickets out']
        runs_left = int(Target) - int(Score)
        balls_left = 120 - (int(Overs_completed) * 6)
        wickets = 10 - int(Wickets_out)
        crr = int(Score) / int(Overs_completed)
        rrr = (runs_left * 6) / balls_left
        input_df = pd.DataFrame(
            {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city],
             'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets], 'total_runs_x': [Target],
             'crr': [crr], 'rrr': [rrr]}
        )
        pipe = pickle.load(open('pipe.pkl', 'rb'))
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        win = str(round(win * 100))
        loss= str(round(loss * 100))

        return render_template('Results.html', win=win,batting_team=batting_team,loss=loss,bowling_team=bowling_team)
if __name__ == '__main__':
    app.run()
