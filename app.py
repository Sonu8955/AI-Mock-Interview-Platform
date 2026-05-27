from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SECRET KEY

app.secret_key = "secretkey"

# DATABASE CONFIG

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# DATABASE MODELS
# =========================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(100))


class Score(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    role = db.Column(db.String(100))

    score = db.Column(db.Integer)


# =========================
# QUESTIONS
# =========================

questions = {

    "Python Developer": [

        "What is the difference between List and Tuple?",

        "Explain OOP concepts in Python.",

        "What is Flask?"

    ],

    "Web Developer": [

        "What is the difference between HTML and HTML5?",

        "Explain CSS Flexbox.",

        "What is JavaScript?"

    ],

    "AI Engineer": [

        "What is Machine Learning?",

        "Explain supervised learning.",

        "Difference between AI and ML?"

    ]
}


# =========================
# HOME PAGE
# =========================

@app.route('/')

def home():

    if 'user' not in session:

        return redirect('/login')

    return render_template('index.html')


# =========================
# SIGNUP PAGE
# =========================

@app.route('/signup', methods=['GET', 'POST'])

def signup():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        existing_user = User.query.filter_by(

            username=username

        ).first()

        if existing_user:

            return "User already exists!"

        user = User(

            username=username,

            password=password

        )

        db.session.add(user)

        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')


# =========================
# LOGIN PAGE
# =========================

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        user = User.query.filter_by(

            username=username,

            password=password

        ).first()

        if user:

            session['user'] = username

            return redirect('/')

        else:

            return "Invalid Username or Password"

    return render_template('login.html')


# =========================
# LOGOUT
# =========================

@app.route('/logout')

def logout():

    session.pop('user', None)

    return redirect('/login')


# =========================
# DASHBOARD PAGE
# =========================

@app.route('/dashboard')

def dashboard():

    if 'user' not in session:

        return redirect('/login')

    user_scores = Score.query.filter_by(

        username=session['user']

    ).all()

    return render_template(

        'dashboard.html',

        scores=user_scores
    )


# =========================
# INTERVIEW PAGE
# =========================

@app.route('/interview', methods=['POST'])

def interview():

    role = request.form['role']

    session['role'] = role

    selected_questions = questions.get(role, [])

    return render_template(

        'result.html',

        role=role,

        questions=selected_questions
    )


# =========================
# SUBMIT ANSWERS
# =========================

@app.route('/submit', methods=['POST'])

def submit():

    feedback = []

    score = 0

    keywords = [

        "python",
        "class",
        "object",
        "function",
        "flask",
        "html",
        "css",
        "javascript",
        "database",
        "sql",
        "api",
        "machine learning",
        "ai",
        "inheritance",
        "encapsulation",
        "polymorphism",
        "algorithm",
        "backend",
        "frontend",
        "framework",
        "server",
        "tuple",
        "list"
    ]

    for question, answer in request.form.items():

        answer = answer.lower()

        matched = 0

        for word in keywords:

            if word in answer:

                matched += 1


        # FEEDBACK SYSTEM

        if len(answer.split()) < 5:

            ai_feedback = f"""

❌ Weak Answer

Question:
{question}

Your answer is too short.

💡 Improvement Tip:
Explain concepts properly with technical terms and examples.
"""

            current_score = 5


        elif matched >= 4:

            ai_feedback = f"""

🚀 Outstanding Answer

Question:
{question}

Excellent technical explanation detected.

✅ Strengths:
• Strong technical vocabulary
• Good explanation
• Clear understanding

💡 Improvement Tip:
Add real-world examples for perfection.
"""

            current_score = 35


        elif matched >= 2:

            ai_feedback = f"""

👍 Good Technical Answer

Question:
{question}

You showed decent technical understanding.

✅ Strengths:
• Technical concepts detected
• Basic clarity present

💡 Improvement Tip:
Add deeper explanation and practical examples.
"""

            current_score = 25


        elif matched >= 1:

            ai_feedback = f"""

🙂 Average Answer

Question:
{question}

Some correct concepts detected but explanation is limited.

💡 Improvement Tip:
Use better technical explanation and examples.
"""

            current_score = 15


        else:

            ai_feedback = f"""

❌ Poor Technical Answer

Question:
{question}

Technical concepts are missing.

💡 Improvement Tip:
Study the topic again and answer with technical keywords.
"""

            current_score = 8


        feedback.append(ai_feedback)

        score += current_score


    # LIMIT SCORE

    if score > 100:

        score = 100


    # SAVE SCORE

    new_score = Score(

        username=session['user'],

        role=session['role'],

        score=score
    )

    db.session.add(new_score)

    db.session.commit()


    return render_template(

        'score.html',

        score=score,

        feedback=feedback
    )


# =========================
# RUN APP
# =========================

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True)