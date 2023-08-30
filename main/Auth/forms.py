from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,EmailField
from wtforms.validators import DataRequired, Length, ValidationError

from flask_login import current_user

from main.models.users import Users

class RegistractionForm(FlaskForm):
    username = StringField('username', validators=[
                                                   DataRequired(), 
                                                   Length(min=2, max=20)
                                                  ])
    
    email = EmailField('email', validators=[DataRequired()])

    password = PasswordField('password', validators=[DataRequired()])

    confirm_password = PasswordField('confirm field', validators=[  
                                                                  DataRequired(), 
                                                                  #EqualTo(password)
                                                                 ])
    
    submit = SubmitField('Signup')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is alredy exist')
        
    
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is alredy exist')




class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])

    password = PasswordField('password', validators=[DataRequired()])

    remember = BooleanField('remember field')

    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email',
                        validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username: # type: ignore
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email: # type: ignore
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')