import os
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session
import json

app = Flask(__name__)


app.secret_key=os.environ["SECRET_KEY"]

numberOfQuestions = os.environ["NUM_QS"]

questions = []

for i in range(1,numberOfQuestions+1):
    inStr = os.environ["Q"+i]

    questions.append(json.loads(inStr))


# {"question":"What is Jake's favorite color?", "A":"Red", "B":"Green", "C":"Gold", "D":"Silver", "correct":"D"}


@app.route("/")
def render_main():
    return render_template('home.html')

@app.route('/question', methods=['GET','POST'])
def renderQuestionPage():
    questionNum = request.args["qnum"]

    question = questions[questionNum-1]

    answers = [question['A'], question['B'], question['C'], question['D']]

    last = True if questionNum == numberOfQuestions else False

    return render_template('question.html', qnum=questionNum, question=question["question"], answers=answers, last=last)




if __name__=="__main__":
    app.run(debug=False, port=54321)
