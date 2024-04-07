from app import app, db

if __name__ == '__main__':
    print("Above if means, I am being run directly (inside run.py), not as an import from another module")
    app.run(debug=True)
