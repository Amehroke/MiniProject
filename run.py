from app import app, db
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    with app.app_context():
        # Create the database and tables
        db.create_all()
    app.run(debug=True)
