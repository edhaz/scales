from app.models import User
from app import db

count = 0
query = User.query.filter_by(completed=True)
for user in query:
    print("Users changed:")
    print(user)
    count += 1

if count == 0:
    print("No users to change.")

for u in query:
    print(u.username)
    u.completed = False

db.session.commit()
print("Session committed")
