from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import bleach
from .forms import RegistrationForm

main = Blueprint('main', __name__, template_folder='templates')

whitelisted_tags = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li']
whitelisted_attributes = {'a': ['href', 'title']}
whitelisted_protocols = ['http', 'https', 'mailto']

warning_message = "Some HTML content was removed for safety"

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

def client_ip():
    # returns real client IP. If behind a proxy, X-Forwarded-For contains original client IP.
    return request.headers.get('X-Forwarded-For', request.remote_addr)

@main.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    bio_html = ""  # default empty bio if GET request

    if form.validate_on_submit():
        raw_bio = form.bio.data or ""  # if bio left empty

        cleaned = bleach.clean(
            raw_bio,
            tags=whitelisted_tags,
            attributes=whitelisted_attributes,
            protocols=whitelisted_protocols,
            strip=True
        )

        # log suspicious HTML removal
        if cleaned != raw_bio:
            current_app.logger.warning(
                "Bio sanitization applied | ip=%s | username=%s",
                client_ip(), form.username.data
            )
            flash(warning_message, "warning")

        bio_html = cleaned

        # log successful registration event
        current_app.logger.info(
            "Registration succeeded | ip=%s | username=%s | email=%s",
            client_ip(), form.username.data, form.email.data
        )

        flash("Registered successfully!", "success")
        return render_template("register.html", form=form, bio_html=bio_html)

    # log validation failures / suspicious attempts
    if request.method == 'POST':
        current_app.logger.warning(
            "Validation failed | ip=%s | username=%s | email=%s | errors=%s",
            client_ip(), form.username.data, form.email.data, dict(form.errors)
        )

    return render_template("register.html", form=form, bio_html=bio_html)
