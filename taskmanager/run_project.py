import os
import sys
import subprocess
import getpass

# Config
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, "venv")
REQUIREMENTS = os.path.join(PROJECT_DIR, "requirements.txt")
DJANGO_MANAGE = os.path.join(PROJECT_DIR, "manage.py")

# Step 1: Create virtual environment if it doesn't exist
if not os.path.exists(VENV_DIR):
    print("Creating virtual environment...")
    subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

# Step 2: Determine python executable inside venv
if os.name == "nt":
    venv_python = os.path.join(VENV_DIR, "Scripts", "python.exe")
else:
    venv_python = os.path.join(VENV_DIR, "bin", "python")

# Step 3: Upgrade pip inside venv
subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])

# Step 4: Install dependencies
if os.path.exists(REQUIREMENTS):
    print("Installing dependencies...")
    subprocess.check_call([venv_python, "-m", "pip", "install", "-r", REQUIREMENTS])
else:
    print("requirements.txt not found. Skipping dependency install.")

# Step 5: Apply migrations
print("Applying migrations...")
subprocess.check_call([venv_python, DJANGO_MANAGE, "migrate"])

# Step 6: Create superuser (optional)
create_superuser = input("Do you want to create a superuser? (y/n): ").lower()
if create_superuser == "y":
    username = input("Username: ")
    email = input("Email: ")
    password = getpass.getpass("Password: ")

    # Create superuser without prompt
    subprocess.check_call([
        venv_python, DJANGO_MANAGE, "createsuperuser",
        "--noinput",
        f"--username={username}",
        f"--email={email}"
    ])

    # Set password manually
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskmanager.settings")  # update project name
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print("Superuser created successfully!")

# Step 7: Run the development server
print("Starting development server at http://127.0.0.1:8000/")
subprocess.call([venv_python, DJANGO_MANAGE, "runserver"])