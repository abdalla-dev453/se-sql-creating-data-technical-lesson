import sqlite3
from datetime import datetime
# import pandas as pd

# Connect to the database 
conn  = sqlite3.connect('my_db.sqlite')
cur = conn.cursor()
print("\nConnected to database")

# ======================
# Step 2: Create Table
# ======================
"""Users table:"""
cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

"""Posts table (belongs to a user)"""
cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
            """)

"""Comments table (belongs to a post and a user)"""
cur.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
            );
            """)
            
conn.commit()
print("\nTable 'users' created with relationships (users -> posts -> comments) (or already exists)")

# ======================
# Step 3: Add data (INSERT)
# ======================
"""Insert users (safe to run multiple times)"""
cur.executemany("""
                INSERT OR IGNORE INTO users (name, email) VALUES(?, ?)
                """, [
                    ('Sofia Ramirez', 'sofia.ramirez@example.com'),
                    ('Devon Blake', 'devon.blake@example.com'),
                    ('Maria Chen', 'maria.chen@example.com'),
                    ('John Doe', 'john.doe@example.com'),
                    ('Bob Smith', 'bob.smith@example.com'),
                    ('Sofia Ramirez', 'sofia.ramirez@example.com'),
                    ('Devon Blake', 'devon.blake@example.com'),
                    ('Maria Chen', 'maria.chen@example.com'),
                    ('John Doe', 'john.doe@example.com'),
                    ('Bob Smith', 'bob.smith@example.com')
                ])
conn.commit()

"""Get user IDS for foreign keys"""
cur.execute("SELECT id, name FROM users;")
users =  dict(cur.fetchall())

"""Insert posts"""
cur.executemany("""
                INSERT INTO posts (user_id, title, content) VALUES(?, ?, ?)
                """, [
                    (list(users.keys())[0], 'My First Blog Post', 'This is the content of my amazing first post...'),
                    (list(users.keys())[1], 'Learning SQL Relationships', 'Foreign keys are very useful...'),
                    (list(users.keys())[2], 'Python and Databases', 'Combining Python with SQLite is powerful!')
                ])
conn.commit()

"""INsert comments"""
cur.executemany("""
                INSERT INTO comments (post_id, user_id, content) VALUES(?, ?, ?)
                """, [
                    (1, 2, 'Great post Sofia!'),
                    (1, 3, 'I learned a lot from this, thanks!'),
                    (2, 1, 'Totally agree, relationships are key in databases.'),
                    (3, 2, 'This is exactly what I needed.')
                ])
conn.commit()
print("\n Sample data inserted into users, posts, and comments tables")


# ======================
#  View data (SELECT)
# ======================
print("\n Users:")
cur.execute("SELECT * FROM users")
for row in cur.fetchall():
    print(row)
    
print("\n Posts with Authors:")
cur.execute("""
            SELECT p.id, p.title, u.name as author, p.created_at
            FROM posts p
            JOIN users u ON p.user_id = u.id;
            """)
for row in cur.fetchall():
    print(row)

print("\n Comments with POst Title and Commenter:")
cur.execute("""
            SELECT c.id, p.title as post_title, u.name as commenter, c.created_at, c.content as comment
            FROM comments c
            JOIN posts p ON c.post_id = p.id
            JOIN users u ON c.user_id = u.id;
            """)
for row in cur.fetchall():
    print(row)

print("\n Comments:")
cur.execute("SELECT * FROM comments")
for comment in cur.fetchall():
    print(comment)
    
# ======================
# Step 4: Modify data (UPDATE)
# ======================
cur.execute("""
            UPDATE comments
            SET content = 'Great first post Sofia! Really inspiring.'
            WHERE id = 1;
            """)
conn.commit()

cur.execute("DELETE FROM posts WHERE id = 2;")
conn.commit()
print("\n Updated a comment and deleted a post (with cascade)")

# Final View
print("\n📋 Remaining data after modifications:")
cur.execute("""
    SELECT p.title, u.name as author 
    FROM posts p JOIN users u ON p.user_id = u.id;
""")
for row in cur.fetchall():
    print(row)
    
    
# Close the connection
conn.close()
print("\n Database Connection closed")