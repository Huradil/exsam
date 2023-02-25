from flask import redirect,render_template,url_for,request,flash
from . import app,db
from .models import Employee,User,Position
from .forms import EmployeeForm,UserForm,PositionForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_user,logout_user,login_required


def index():
    employees=Employee.query.all()
    return render_template('index.html',employees=employees)


def position_create():
    form=PositionForm()
    if request.method=='POST':
        if form.validate_on_submit():
            position=Position()
            form.populate_obj(position)
            db.session.add(position)
            db.session.commit()
            flash('успешно','success')
        else:
            flash('ошибка','danger')
            return render_template('standart_form.html',form=form)
    return render_template('standard_form.html',form=form)


def employee_create():
    form=EmployeeForm()
    form.position_id.choices=[(g.id, g.name) for g in Position.query.order_by('name')]
    if request.method=='POST':
        if form.validate_on_submit():
            employee=Employee()
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('успешно','success')
        else:
            flash('ошибка','danger')
            return render_template('standard_form.html',form=form)
    return render_template('standard_form.html',form=form)



def employee_update(id):
    employee=Employee.query.get(id)
    form=EmployeeForm(obj=employee)
    if request.method=='POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print(form.errors)
    return render_template('standard_form.html',form=form)





def employee_delete(id):
    employee=Employee.query.get(id)
    if request.environ=='POST':
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confirm_delete.html',employee=employee)

def register():
    form=UserForm()
    if request.method=='POST':
        if form.validate_on_submit():
            user=User()
            form.populate_obj(user)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                flash('такой пользователь уже существует','danger')
            else:
                flash('успешно','success')
        else:
            print(form.errors)
    return render_template('user_form.html',form=form)





def login():
    form=UserForm()
    if request.method=='POST':
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('неправильные данные','danger')
                print(form.errors)
        else:
            print(form.errors)
    return render_template('user_form.html',form=form)



def logout():
    logout_user()
    return redirect(url_for('login'))
