from app import app, db

if __name__ == '__main__':
    print("Above if means, I am being run directly (inside run.py), not as an import from another module")
    with app.app_context():
        # Create the database and tables 
        db.create_all()
    app.run(debug=True)
