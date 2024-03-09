python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install django pillow djangorestframework djangorestframework_simplejwt

python manage.py migrate

if [ ! -f "secret_key.py" ]; then
    echo "Generating Django secret key..."
    echo "SECRET_KEY='$(python -c 'import random; import string; print("".join(random.SystemRandom().choices(string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"))[:50])')'" > secret_key.py
fi

echo "Configuring Django project settings..."

if [ ! -f "OneOnOne/settings_local.py" ]; then
    cp OneOnOne/settings_local.example.py OneOnOne/settings_local.py
fi

sed -i "s/'NAME': 'db_name',/'NAME': 'your_database_name',/g" OneOnOne/settings_local.py
sed -i "s/'USER': 'db_user',/'USER': 'your_database_user',/g" OneOnOne/settings_local.py
sed -i "s/'PASSWORD': 'db_password',/'PASSWORD': 'your_database_password',/g" OneOnOne/settings_local.py
sed -i "s/'HOST': 'localhost',/'HOST': 'your_database_host',/g" OneOnOne/settings_local.py
sed -i "s/'PORT': '5432',/'PORT': 'your_database_port',/g" OneOnOne/settings_local.py

sed -i "/INSTALLED_APPS = \[/a \ \ \ \ 'rest_framework'," OneOnOne/settings_local.py
sed -i "/INSTALLED_AP
