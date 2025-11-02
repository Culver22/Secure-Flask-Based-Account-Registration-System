import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp

blacklisted_usernames = ['admin', 'root', 'superuser']
blacklisted_passwords = ['password123', 'admin', '123456', 'qwerty', 'letmein', 'welcome', 'iloveyou',
                         'abc123', 'monkey', 'football']

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

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )

    bio = TextAreaField("Bio / Comment")
    submit = SubmitField("Register")

    def validate_username(self, field):
        if field.data.strip().lower() in blacklisted_usernames:
            raise ValidationError("Username is blacklisted, Please choose another.")

    def validate_password(self, field):
        password = field.data
        lowercase_password = password.lower()
        username = self.username.data.lower()
        email = self.email.data.lower()

        # Blacklisted common password condition
        if lowercase_password in blacklisted_passwords:
            raise ValidationError("Password is common, please choose a stronger password.")

        # General password conditions
        if len(password) < 12:
            # Length 12 or over
            raise ValidationError("Password must be at least 12 characters long.")
        if not re.search(r"[A-Z]", password):
            # Capital letter
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            # Lowercase letter
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            # Number
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r"[^A-Za-z0-9]", password):
            # Special character
            raise ValidationError("Password must contain at least one special character.")
        if re.search(r"\s", password):
            # Whitespace
            raise ValidationError("Password must not contain any whitespace.")

        # Username conditions
        if username in lowercase_password:
            raise ValidationError("Password must not contain the username")

        # Full email check
        if email in lowercase_password:
            raise ValidationError("Password must not contain the email")

        # Partial email check
        parts = email.split("@")
        local_part = parts[0]
        domain_part = parts[1]

        # Check username/local-part of email address
        if local_part != "" and local_part in lowercase_password:
            raise ValidationError("Password must not contain parts of the email (username).")

        # Check email domain
        primary_domain = domain_part.split(".",1)[0]
        if primary_domain != "" and primary_domain in lowercase_password:
            raise ValidationError("Password must not contain parts of the email (domain).")

