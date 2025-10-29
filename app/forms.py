from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, regexp

blacklist = ['admin', 'root', 'superuser']  #

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            # server-side required
            Length(min=3, max=30, message="Must be 3–30 characters."),
            # length constraint of 30 max characters
            Regexp(r"^[A-Za-z_]+$", message="Only letters and underscores allowed."),
            # Only allows letters (including capitals) and underscores
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            # server-side required
            Regexp( r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:edu|ac\.uk|org)$',
                    message="Email must follow standard email format. Only domains expected: .edu, .ac.uk and .org"),
            # always confirms the correct email format, also makes sure of an @ and the allowed domains
        ]
    )
    # Todo add complexity rules in part B
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )

    bio = TextAreaField("Bio / Comment")
    submit = SubmitField("Register")

    def validate_username(self, username):
        if username.data.strip().lower() in blacklist:
            raise ValidationError("Username is blacklisted, Please choose another.")