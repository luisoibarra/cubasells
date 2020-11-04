if [ ! -f "db.sqlite3" ]; # BD doesnt exist 
then
    python3 manage.py migrate
fi

# Fill database group table
python3 manage.py loaddata fixtures/group_fixture.json

USERNAME=admin
PASSWORD=administrator123
EMAIL="luise98cu@gmail.com"

# Create superuser
python3 manage.py createsuperuserpass --no-input --username $USERNAME --password $PASSWORD --email $EMAIL
