# 🚀 BlogSphere - Modern Publishing & Discussion Platform

A full-featured, responsive blogging platform built with **Flask**, **SQLAlchemy**, **SQLite**, and styled with modern dark-mode **Tailwind CSS**, **Lucide Icons**, and **Marked.js**.

---

## ✨ Features

- **👤 Authentication & User Profiles**
  - Secure registration & login with Werkzeug password hashing.
  - Custom user profiles with customizable avatar accent colors and bio.
  - Profile showcase displaying all articles authored by each user.

- **✍️ Article Authoring & Publishing**
  - Interactive split/live preview Markdown editor.
  - Custom topic categorization (*Technology, Engineering, Design, AI, Career, Tutorials, Life & Culture*).
  - Preset cover images selector or custom image URLs.
  - Automatic reading time calculation and excerpt generator.
  - Full author-only edit and delete controls.

- **💬 Threaded Discussion & Commenting**
  - Multi-level nested comments & reply threads.
  - Author badge distinction for post authors participating in discussions.
  - Comment moderation: comment authors or post owners can delete comments.

- **❤️ Interactive Post Reactions & Discovery**
  - Asynchronous (AJAX) heart/like toggling with real-time counter updates.
  - Search filter querying titles, excerpts, and post markdown content.
  - Filter tabs by categories with responsive horizontal scrolling.
  - Dynamic hero post highlighting trending articles.

---

## 🛠️ Project Structure

```
blogplatform/
├── app/
│   ├── __init__.py           # Flask app factory, custom Jinja filters, context processors
│   ├── models.py             # User, Post, Comment, PostLike models
│   ├── routes/
│   │   ├── auth.py           # Register, login, logout, profile & edit profile
│   │   ├── blog.py           # Feed, post detail, post CRUD, search, likes
│   │   └── comments.py       # Comment submission, replies, and deletion
│   ├── templates/
│   │   ├── base.html         # Base template with glass navbar, notifications & footer
│   │   ├── index.html        # Feed with hero showcase, category tabs, and post cards
│   │   ├── post_detail.html  # Full article view, markdown, likes, and comments stream
│   │   ├── post_editor.html  # Split-screen Markdown editor with live preview
│   │   ├── login.html        # Sign-in form
│   │   ├── register.html     # Registration form
│   │   ├── profile.html      # Public user profile & articles feed
│   │   └── profile_edit.html # Profile settings & avatar color customizer
│   └── static/
│       ├── css/custom.css    # Custom dark theme, typography & animations
│       └── js/main.js        # Markdown live preview, AJAX likes, reply toggles
├── tests/
│   └── test_blog.py          # Comprehensive automated unit & integration test suite
├── config.py                 # Configuration & SQLite database URI
├── seed.py                   # Realistic seed data (users, articles, comments, likes)
├── run.py                    # Server runner with automatic database init
└── README.md                 # Documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Flask and Flask-SQLAlchemy

### 2. Seed Sample Data (Optional)
To populate the database with realistic sample posts, users, comments, and replies:
```powershell
python seed.py
```

### 3. Start the Server
```powershell
python run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Demo Accounts

The seed script initializes three accounts for testing:

| Username | Password | Role |
| :--- | :--- | :--- |
| `tech_writer` | `password123` | Backend Architect & Writer |
| `sarah_dev` | `password123` | UI/UX Designer & Writer |
| `alex_ai` | `password123` | AI Researcher & Writer |

You can also register a brand-new account through the `/register` page!

---

## 🧪 Running Tests

Run the complete test suite:
```powershell
python -m unittest discover tests
```
All 9 automated unit & integration tests verify:
- Registration, login, and invalid credentials rejection
- Post creation, display, editing, and unauthorized edit rejection
- Post deletion permissions
- Comment creation, nested replies, and moderation permissions
- AJAX post liking and count toggling
- Category filtering and search queries
