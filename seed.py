import sys
from app import create_app
from app.models import db, User, Post, Comment, PostLike
from app.routes.blog import slugify

def seed_database():
    app = create_app()
    with app.app_context():
        print("Resetting and seeding database...")
        db.drop_all()
        db.create_all()

        # 1. Create Users
        users_data = [
            {
                "username": "tech_writer",
                "email": "tech@example.com",
                "password": "password123",
                "bio": "Senior Backend Architect & open-source enthusiast. Writing about distributed systems, Python performance, and modern cloud design.",
                "avatar_color": "indigo"
            },
            {
                "username": "sarah_dev",
                "email": "sarah@example.com",
                "password": "password123",
                "bio": "Frontend designer & engineering lead. Passionate about component systems, responsive micro-interactions, and accessibility.",
                "avatar_color": "rose"
            },
            {
                "username": "alex_ai",
                "email": "alex@example.com",
                "password": "password123",
                "bio": "AI researcher & engineer exploring generative models, autonomous agents, and next-generation programming interfaces.",
                "avatar_color": "emerald"
            }
        ]

        users = {}
        for u in users_data:
            user = User(
                username=u["username"],
                email=u["email"],
                bio=u["bio"],
                avatar_color=u["avatar_color"]
            )
            user.set_password(u["password"])
            db.session.add(user)
            users[u["username"]] = user

        db.session.commit()
        print(f"Created {len(users)} users.")

        # 2. Create Blog Posts
        posts_data = [
            {
                "title": "Architecting Scalable Web Applications with Modern Python",
                "category": "Technology",
                "cover_image": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "A deep dive into writing maintainable, high-performance web systems using modular patterns, database indexing, and asynchronous job queues.",
                "content": """## Introduction

Building web applications that can scale from ten users to millions requires intentional architectural choices right from day one. In this guide, we will explore fundamental practices that keep your Python codebases clean, responsive, and robust.

### 1. Decouple Your Architecture

One common pitfall is tightly coupling your data models with your presentation layer. By employing the **Application Factory** pattern and modular blueprints, you isolate domain logic:

```python
from flask import Flask
from app.extensions import db

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    return app
```

### 2. Database Optimization & Indexing

Always ensure your foreign keys and frequently queried fields (such as `slug`, `username`, and `created_at`) have database indices. Unindexed queries might seem fast during development, but they quickly lead to full table scans as dataset sizes grow.

> "Premature optimization is the root of all evil, but neglected indexing is the root of database downtime."

### 3. Asynchronous Tasks

Offload heavy work (sending emails, image processing, analytics aggregation) to background queues using tools like Celery or Redis Queue. Your HTTP request-response cycle should always remain brisk and lightweight.

### Summary

Simplicity combined with strong architectural boundaries is the hallmark of resilient systems. Keep dependencies minimal, leverage ORM relationships wisely, and always measure before optimizing!
""",
                "author": users["tech_writer"]
            },
            {
                "title": "Crafting Modern User Experiences: Design Principles That Truly Work",
                "category": "Design",
                "cover_image": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "Discover how subtle typography choices, deliberate whitespace, and thoughtful micro-interactions transform good interfaces into unforgettable products.",
                "content": """## What Makes an Interface Delightful?

Great user interfaces don't draw attention to themselves; instead, they empower users to accomplish their goals effortlessly. Here are key principles we adhere to when crafting digital experiences.

### 1. Visual Hierarchy & Contrast

Ensure the most important action on any screen stands out immediately:
- **Primary Actions**: High contrast, vibrant button styling.
- **Secondary Actions**: Subtle outlines or muted backgrounds.
- **Danger Actions**: Clear cautionary coloring with confirmation guards.

### 2. The Power of Typography

Typography is 90% of web design. Pairing a clean geometric sans-serif (like *Inter*) with consistent line-heights creates an inviting reading atmosphere.

```css
/* Generous line-height for effortless reading */
.article-body {
  line-height: 1.85;
  letter-spacing: -0.01em;
}
```

### 3. Meaningful Micro-interactions

Hover states, active button scales, and smooth fade-in toasts provide sensory confirmation that the system is responding to the user's intent. When done tastefully, micro-interactions breathe life into static web pages.
""",
                "author": users["sarah_dev"]
            },
            {
                "title": "The Rise of Autonomous AI Agents in Software Engineering",
                "category": "Artificial Intelligence",
                "cover_image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "How multi-agent systems, tool calling, and cognitive loops are fundamentally revolutionizing the way software is conceived, coded, and maintained.",
                "content": """## The Shift from Autocomplete to Autonomous Pair Programmers

The frontier of developer tools has shifted rapidly from simple code completion to goal-oriented, multi-step agentic systems capable of planning, executing, and self-verifying software systems.

### Core Anatomy of an Agent Loop

An autonomous coding agent operates in a continuous observation-reasoning-action loop:
1. **Perception**: Inspecting repository structure, git logs, and runtime errors.
2. **Reasoning & Planning**: Formulating an implementation plan and identifying edge cases.
3. **Tool Execution**: Calling file manipulation tools, running terminal commands, and reading output.
4. **Verification**: Executing test suites and performing end-to-end sanity checks.

```mermaid
graph TD
    User([User Request]) --> Planner[Planner & Reasoning Agent]
    Planner --> Tools[Code & System Tools]
    Tools --> Test[Automated Test Suite]
    Test --> Verified{Tests Pass?}
    Verified -- No --> Planner
    Verified -- Yes --> Output([Deliver Solution])
```

### The Future of Engineering

Software engineers are becoming systems conductors—orchestrating AI agents, defining high-level specifications, and reviewing architectural integrity.
""",
                "author": users["alex_ai"]
            },
            {
                "title": "Mastering the Art of Code Reviews: Practical Wisdom for Teams",
                "category": "Engineering",
                "cover_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "Learn how to conduct insightful, constructive code reviews that elevate team velocity, nurture engineering culture, and keep bugs out of production.",
                "content": """## Why Code Reviews Matter

Code review is not merely a gatekeeping exercise; it is an invaluable opportunity for collective knowledge sharing, mentorship, and continuous architecture refinement.

### Rules of Thumb for Reviewers

- **Focus on the big picture first**: Does this architecture make sense? Are concurrency, security, and edge cases handled?
- **Automate formatting and linting**: Never waste human review time arguing over indentation or semicolons—let automated CI tools enforce formatting.
- **Be kind and specific**: Instead of *"This code is messy"*, try *"Could we extract this loop into a helper function to improve readability and testability?"*.

### Rules of Thumb for Authors

- Keep pull requests small and focused (ideally under 300 lines).
- Provide a clear summary and screenshots or verification steps.
- Welcome feedback as an opportunity for mutual growth.
""",
                "author": users["tech_writer"]
            }
        ]

        created_posts = []
        for p in posts_data:
            post = Post(
                title=p["title"],
                slug=slugify(p["title"]),
                category=p["category"],
                cover_image=p["cover_image"],
                excerpt=p["excerpt"],
                content=p["content"],
                author_id=p["author"].id
            )
            db.session.add(post)
            created_posts.append(post)

        db.session.commit()
        print(f"Created {len(created_posts)} blog posts.")

        # 3. Add Comments & Replies
        comments_data = [
            {
                "post": created_posts[0],
                "author": users["sarah_dev"],
                "content": "Fantastic breakdown! Totally agree with decoupling the architecture early. It saves countless hours when scaling later."
            },
            {
                "post": created_posts[0],
                "author": users["alex_ai"],
                "content": "Database indexing on slug and foreign keys is so frequently overlooked. Glad you highlighted that!"
            },
            {
                "post": created_posts[1],
                "author": users["tech_writer"],
                "content": "The section on typography and generous line heights hits the nail on the head. Visual comfort makes a huge difference."
            },
            {
                "post": created_posts[2],
                "author": users["tech_writer"],
                "content": "The agent loop diagram clarifies the cognitive cycle nicely. Exciting times for software development."
            }
        ]

        top_comments = []
        for c in comments_data:
            comment = Comment(
                content=c["content"],
                post_id=c["post"].id,
                author_id=c["author"].id
            )
            db.session.add(comment)
            top_comments.append(comment)

        db.session.commit()

        # Add replies
        reply_1 = Comment(
            content="Thanks Sarah! Modularity really pays dividends when migrating components or adding new background workers.",
            post_id=created_posts[0].id,
            author_id=users["tech_writer"].id,
            parent_id=top_comments[0].id
        )
        reply_2 = Comment(
            content="Appreciate it Alex! Next post will cover query optimization strategies with SQLAlchemy.",
            post_id=created_posts[0].id,
            author_id=users["tech_writer"].id,
            parent_id=top_comments[1].id
        )
        db.session.add_all([reply_1, reply_2])

        # 4. Add Likes
        likes = [
            PostLike(user_id=users["sarah_dev"].id, post_id=created_posts[0].id),
            PostLike(user_id=users["alex_ai"].id, post_id=created_posts[0].id),
            PostLike(user_id=users["tech_writer"].id, post_id=created_posts[1].id),
            PostLike(user_id=users["sarah_dev"].id, post_id=created_posts[2].id),
            PostLike(user_id=users["alex_ai"].id, post_id=created_posts[3].id),
            PostLike(user_id=users["sarah_dev"].id, post_id=created_posts[3].id),
        ]
        db.session.add_all(likes)

        db.session.commit()
        print("Database successfully seeded with users, posts, comments, replies, and likes!")

if __name__ == "__main__":
    seed_database()
