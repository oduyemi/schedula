from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, EmailField
from wtforms.validators import DataRequired, length, Regexp, EqualTo, ValidationError, Email
from schedula_app.model import User

class ContactForm(FlaskForm):
    contact_name = StringField("contact_name",
        validators=[
            DataRequired(),
            length(min=2, max=30, message = "Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z.]*$", 0, "Your Last name must contain only letters")],
        render_kw={"placeholder": "Your name"})

    mail = EmailField("mail",
        validators=
            [DataRequired(),
            Email(),    
            Email(message="Please provide a valid email address")],
            render_kw={"placeholder": "Email address"})

    phone = StringField("phone",
        validators=[
            DataRequired(),
            length(min=2, max=50, message = "Please provide a valid name")],
        render_kw={"placeholder": "Phone number"})

    message = TextAreaField("message",
        validators=[
            DataRequired(),
            length(min=3, max=1000, message = "Please provide a valid name")],
        render_kw={"placeholder": "Your text here..."})
    
    submit = SubmitField("Send Message")


class LoginForm(FlaskForm):
    phone = StringField("phone",
        validators=[
            DataRequired(),
            length(min=1, max=20, message = "Please provide a valid phone number"),
            Regexp(
                "^[A-Za-z] [A-Za-a0-9.]*", 0, "Please provide a valid phone number")],
        render_kw={"placeholder": "Enter your phone number"})

    password = PasswordField("password",
        validators=
            [DataRequired(),
            length(min=8, max=20)],
            render_kw={"placeholder": "Enter your password"})
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")




class UserRegForm(FlaskForm):
    fname = StringField("fname",
    validators=[
        DataRequired(),
        length(min=1, max=20, message = "Please provide a valid name"),
        Regexp(
            "^[A-Za-z]x*", 0, "Your first name must contain only letters"
            ),
        ],
    render_kw={"placeholder": "Your first name"})

    lname = StringField("lname",
    validators=[
        DataRequired(),
        length(min=1, max=20, message = "Please provide a valid name"),
        Regexp(
            "^[A-Za-z]x*", 0, "Your last name must contain only letters"
            ),
        ],
    render_kw={"placeholder": "Your last name"})

    phone = StringField("phone",
        validators=[
            DataRequired(),
            length(min=1, max=20, message = "Please provide a valid phone number"),
            Regexp(
                "^[A-Za-z] [A-Za-a0-9.]*", 0, "Please provide a valid phone number")],
        render_kw={"placeholder": "Enter your phone number"})

    password = PasswordField("password",
        validators=
            [DataRequired(),
            length(min=6, max=20)],
            render_kw={"placeholder": "Enter your password"})

    confirm_password = PasswordField("confirm_password",
        validators=
            [DataRequired(),
            length(min=6, max=20)],
            render_kw={"placeholder": "Confirm your password"})
    EqualTo("password", message = "The passwords must match! ")
    submit = SubmitField("Sign Up")

    def validate_phone(self, phone):
        user = User.query.filter_by(user_phone = phone.data).first()
        if user:
            raise ValidationError("That Phone number is already registered. Please choose a different one.")

class PhoneForm(FlaskForm):
    phone = StringField("phone",
        validators=[
            DataRequired(),
            length(min=2, max=50, message = "Please provide a valid name")],
            render_kw={"placeholder": "Phone number"})
    submit = SubmitField("Update")


