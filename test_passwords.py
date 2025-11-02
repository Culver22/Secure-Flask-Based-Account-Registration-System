from app import create_app
from app.forms import RegistrationForm

def test_password(password, username="Ollie", email="Ollie@newcastle.edu"):
    # Disable CSRF for this unit-style test (no HTTP POST here)
    form = RegistrationForm(
        meta={"csrf": False},
        data={
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": password,
            "bio": ""
        }
    )
    if form.validate():
        print(f"VALID:   {password}")
    else:
        print(f"INVALID: {password}")
        # show only password-related errors for brevity
        print(form.errors.get("password"))

if __name__ == "__main__":
    app = create_app()
    with app.app_context():  # <-- pushes current_app so Flask-WTF can read config
        # good example
        test_password("StrongPass99!")

        # too short
        test_password("Short1!")

        # no uppercase
        test_password("password123!")

        # no digit
        test_password("Password!!!!")

        # no special
        test_password("Password1234")

        # whitespace fail
        test_password("Strong Pass99!")

        # contains username
        test_password("Olliepassword123!")

        # contains email
        test_password("NewcastleeduPassword123!")

        # blacklist
        test_password("password123")
