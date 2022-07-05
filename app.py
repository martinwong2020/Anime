from flask import Flask,render_template,request,redirect,url_for
from anime_rec import anime_recommendation
app=Flask(__name__)


@app.route('/',methods=["GET","POST"])
def home():
    if request.method=="POST":
        userInput=request.form['anime']
        anime=anime_recommendation(userInput)
        print("ANIME",anime)
        return render_template("main.html",anime_one=anime[0],anime_two=anime[1],anime_three=anime[2],anime_four=anime[3],anime_five=anime[4])
    return render_template("home.html")


if __name__== '__main__':
    app.run(debug=True,port=8000)
