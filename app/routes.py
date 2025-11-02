from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import bleach
from .forms import RegistrationForm

main = Blueprint('main', __name__)

whitelisted_tags = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li']
whitelisted_attributes = {'a': ['href', 'title']}
whitelisted_protocols = ['http', 'https', 'mailto']

warning_message = "Some HTML content was removed for safety"

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

def client_ip():
    # Returns real client IP, if behing a proxy use X-forwarded-For first
    return request.headers.get('X-Forwarded-For', request.remote_addr)

@main.route('/register', methods=['GET', 'POST'])
def register():
    name = request.form.get('name') if request.method == 'POST' else ''
    return render_template('register.html', name=name)