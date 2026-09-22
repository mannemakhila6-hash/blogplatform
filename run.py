import os
from app import create_app
from app.models import db, User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Check if database has any users; if not, auto-seed with sample content
        if User.query.count() == 0:
            print("No users found. Initializing seed data...")
            from seed import seed_database
            seed_database()

    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 BlogSphere is running at http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)
