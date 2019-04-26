import os
from flask import Flask, url_for, render_template, request, redirect, flash
from flask import redirect
from flask import session
import json

app = Flask(__name__)


app.secret_key=os.environ["SECRET_KEY"]

numberOfQuestions = int(os.environ["NUM_QS"])

questions = []

for i in range(1,numberOfQuestions+1):
    inStr = os.environ["Q%i" % i]

    questions.append(json.loads(inStr))


# {"question":"What is Jake's favorite color?", "A":"Red", "B":"Green", "C":"Gold", "D":"Silver", "correct":"D"}


@app.route("/")
def render_main():
    session["score"] = 0
    session["finished"] = 0
    session["has_answered"] = [False for _ in range(numberOfQuestions)]

    if "did_cheat" in session and session["did_cheat"]:
        flash("NO CHEATING!")
        session["did_cheat"] = False

    return render_template('home.html')

@app.route('/question', methods=['GET','POST'])
def renderQuestionPage():
    if session["finished"] == 1:
        redirect(url_for(".render_main"))

    if "answer" in request.form:
        oldQuestionNum = int(request.args["qnum"]) -1
        oldQ = questions[oldQuestionNum-1]

        if session["has_answered"][oldQuestionNum]:
            session["did_cheat"] = True
            redirect(url_for(".render_main"))

        session["has_answered"][oldQuestionNum] = True

        if oldQ["correct"] == request.form["answer"]:
            session["score"] = session["score"] + 1

        print("Question #%i: Correct answer: %s || Inputted answer: %s" % (oldQuestionNum, oldQ["correct"], request.form["answer"]))

    questionNum = int(request.args["qnum"])
    question = questions[questionNum-1]

    answers = [question['A'], question['B'], question['C'], question['D']]

    last = True if questionNum == numberOfQuestions else False
    return render_template('question.html', qnum=questionNum, question=question["question"], answers=answers, last=last)

@app.route("/finPage", methods=['GET', 'POST'])
def render_finPage():
    if "answer" in request.form:
        oldQuestionNum = numberOfQuestions
        oldQ = questions[oldQuestionNum-1]

        if oldQ["correct"] == request.form["answer"]:
            session["score"] = session["score"] + 1

    session["finished"] = 1

    return render_template('finPage.html', score = session['score'])




if __name__=="__main__":
    app.run(debug=False, port=54321)
