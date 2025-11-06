import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from flask import current_app

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
            # log blacklisted username attempt
            current_app.logger.warning("Blacklisted username attempt | username=%s", field.data.strip())
            raise ValidationError("Username is blacklisted, Please choose another.")

    def validate_email(self, field):
        # log invalid domain attempt
        email = (field.data or "").strip().lower()
        if not (email.endswith(".edu") or email.endswith(".ac.uk") or email.endswith(".org")):
            current_app.logger.warning("Invalid email domain attempt | username=%s | email=%s",
                           (self.username.data or "").strip(), email)

    def validate_password(self, field):
        password = field.data
        lowercase_password = password.lower()
        username = self.username.data.lower()
        email = self.email.data.lower()

        # blacklisted password condition
        if lowercase_password in blacklisted_passwords:
            raise ValidationError("Password is common, please choose a stronger password.")

        # general password conditions
        if len(password) < 12:
            # length 12 or over
            raise ValidationError("Password must be at least 12 characters long.")
        if not re.search(r"[A-Z]", password):
            # capital letter
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            # lowercase letter
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            # number
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[^A-Za-z0-9]", password):
            # special character
            raise ValidationError("Password must contain at least one special character.")
        if re.search(r"\s", password):
            # whitespace
            raise ValidationError("Password must not contain any whitespace.")

        # username conditions
        if username in lowercase_password:
            raise ValidationError("Password must not contain the username")

        # full email check
        if email in lowercase_password:
            raise ValidationError("Password must not contain the email")

        # partial email check
        parts = email.split("@")
        # regex for email will always ensure there will be two parts, hence not using a guard as there
        # won't be an IndexError
        local_part = parts[0]
        domain_part = parts[1]

        # check username/local-part of email address
        if local_part != "" and local_part in lowercase_password:
            raise ValidationError("Password must not contain parts of the email (local-part).")

        # check email domain
        primary_domain = domain_part.split(".",1)[0]
        if primary_domain != "" and primary_domain in lowercase_password:
            raise ValidationError("Password must not contain parts of the email (domain).")

