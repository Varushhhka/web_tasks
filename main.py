from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_restful import abort
from werkzeug.utils import redirect

from data import db_session
from data.departments import Department
from data.jobs import Jobs
from data.user import User
from forms.departments import DepartmentsForm
from forms.jobs import JobsForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@app.route('/departments')
def department():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template("departments.html", departments=departments)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Req',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.start_date = form.start_date.data
        jobs.end_date = form.end_date.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Adding a job', form=form)


@app.route('/new_department',  methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.members = form.members.data
        dep.email = form.email.data
        current_user.deps.append(dep)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('new_department.html', title='Adding a department', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.user == current_user |
                                                          current_user.id == id)).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.start_date.data = jobs.start_date
            form.end_date.data = jobs.end_date
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.start_date = form.start_date.data
            jobs.end_date = form.end_date.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html', title='Editing a work', form=form)


@app.route('/new_departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_departments(id):
    form = DepartmentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        deps = db_sess.query(Department).filter(Department.id == id, Department.user == current_user).first()
        if deps:
            form.title.data = deps.title
            form.members.data = deps.members
            form.email.data = deps.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        deps = db_sess.query(Department).filter(Department.id == id, Department.user == current_user).first()
        if deps:
            deps.title = form.title.data
            deps.members = form.members.data
            deps.email = form.email.data
            return redirect('/departments')
        else:
            abort(404)
    return render_template('new_department.html', title='Editing a department', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.user == current_user |
                                                      current_user.id == id)).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    deps = db_sess.query(Department).filter(Department.id == id, Department.user == current_user).first()
    if deps:
        db_sess.delete(deps)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()