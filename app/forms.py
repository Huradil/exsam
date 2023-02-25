from flask_wtf import FlaskForm
import wtforms as wf


class PositionForm(FlaskForm):
    name=wf.StringField(label='имя',validators=[
        wf.validators.DataRequired()
    ])
    department=wf.StringField(label='отдел')
    wage=wf.IntegerField(label='зарплата',validators=[
        wf.validators.DataRequired()
    ])

    def validate_wage(self,field):
        if field.data<0:
            raise wf.validators.ValidationError('значеение не должно быть отрицательным')



class EmployeeForm(FlaskForm):
    name=wf.StringField(label='имя',validators=[
        wf.validators.DataRequired()
    ])
    inn=wf.StringField(label='инн',validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=14,max=14,)
    ])
    position_id=wf.SelectField(label='должность',coerce=int)

    def validate_inn(self,field):
        if not field.data.startswith('1') and not field.data.startswith('2'):
            raise wf.validators.ValidationError('инн должен начинаться на 1 или 2')



class UserForm(FlaskForm):
    username=wf.StringField(label='имя пользователя',validators=[
        wf.validators.DataRequired()
    ])
    password=wf.PasswordField(label='пароль',validators=[
        wf.validators.DataRequired()
    ])
