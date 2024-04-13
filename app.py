from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

# Basic setup of an app with db connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#  Class for table with deadlines
class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(300))
    description = db.Column(db.String(300))
    date = db.Column(db.String(10))

    def __repr__(self):
        return '<Deaedline %r>' % self.id

    def to_dict_deadlines(self):
        data = {
            'id': self.id,
            'subject': self.subject,
            'description': self.description,
            'date': self.date,
        }
        return data


#  Class for table with schedule
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    type = db.Column(db.String(300))
    place = db.Column(db.String(300))
    teacher = db.Column(db.String(300))
    date = db.Column(db.Integer)
    how_often = db.Column(db.Integer)

    def __repr__(self):
        return '<Schedule %r>' % self.id

    def to_dict_schedule(self):
        data = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'place': self.place,
            'teacher': self.teacher,
            'date': self.date,
            'how_often': self.how_often
        }
        return data


# Main page generation
@app.route('/')
def index():
    return render_template('index.html')


# Page which gives a json file with schedule (needed for an Android app)
@app.route("/get-schedule", methods=["GET"])
def get_schedule():
    subjects_list = []
    data = Schedule.query.all()

    for subject in data:
        subjects_list.append(subject.to_dict_schedule())

    # returning json-file
    return jsonify(subjects_list)


# Page which gives a json file with all deadlines (needed for an Android app)
@app.route("/get-deadlines", methods=["GET"])
def get_deadlines():
    subjects_list = []
    data = Deadline.query.all()

    for subject in data:
        subjects_list.append(subject.to_dict_deadlines())

    # returning json-file
    return jsonify(subjects_list)


# Page with schedule creation form
@app.route('/create-schedule', methods=['POST', 'GET'])
def create_schedule():
    # Adding new record to schedule table
    if request.method == 'POST':

        # taking info from form
        name = request.form['name']
        type = request.form['type']
        place = request.form['place']
        teacher = request.form['teacher']
        date = request.form['date']
        how_often = request.form['how_often']

        schedule = Schedule(name=name, type=type, place=place, date=date, teacher=teacher,
                            how_often=int(how_often))
        # adding record to a table
        try:
            db.session.add(schedule)
            db.session.commit()
            return redirect('/schedule')  # redirecting to a schedule page

        except:
            return 'Something goes wrong'

    # Loading page with schedule creation form
    else:
        return render_template('create-schedule.html')


# Page with deadline creation form
@app.route('/create-deadlines', methods=['POST', 'GET'])
def create_deadlines():
    # Adding new record to deadline table
    if request.method == 'POST':

        # taking info from form
        subject = request.form['subject']
        description = request.form['description']
        date = request.form['date']

        deadline = Deadline(subject=subject, description=description, date=date)

        # adding record to a table
        try:
            db.session.add(deadline)
            db.session.commit()
            return redirect('/deadlines')

        except:
            return 'Something goes wrong'

    # Loading page with deadline creation form
    else:
        return render_template('create-deadlines.html')


# Page with schedule list
@app.route('/schedule')
def schedule():
    schedule = Schedule.query.all()

    return render_template('schedule.html', schedule=schedule)


# Page with detailed info of concrete schedule record
@app.route('/schedule/<int:id>')
def schedule_detail(id):
    schedule_detail = Schedule.query.get(id)

    return render_template('schedule_detail.html', schedule_detail=schedule_detail)


# Functional page for schedule record deleting
@app.route('/schedule/<int:id>/delete')
def schedule_delete(id):
    schedule_detail = Schedule.query.get_or_404(id)

    try:
        db.session.delete(schedule_detail)
        db.session.commit()
        return redirect('/schedule')

    except:
        return 'Something goes wrong'


# Page with deadline list
@app.route('/deadlines')
def deadline():
    deadline = Deadline.query.all()

    return render_template('deadline.html', deadline=deadline)


# Page with detailed info of concrete deadline
@app.route('/deadline/<int:id>')
def deadline_detail(id):
    deadline_detail = Deadline.query.get(id)

    return render_template('deadline_detail.html', deadline_detail=deadline_detail)


# Functional page for deadline record deleting
@app.route('/deadline/<int:id>/delete')
def deadline_delete(id):
    deadline_detail = Deadline.query.get_or_404(id)

    try:
        db.session.delete(deadline_detail)
        db.session.commit()
        return redirect('/deadline')

    except:
        return 'Something goes wrong'


if __name__ == '__main__':
    app.run(debug=False)
