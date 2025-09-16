from app import create_app, db

app = create_app()

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()

if __name__ == '__main__':
    init_db()  # Initialize database
    app.run(debug=True)