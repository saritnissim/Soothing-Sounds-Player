import psycopg2
from dotenv import load_dotenv
import os


# Load environment variables from the .env file
load_dotenv()

class DatabaseManager:
    def __init__(self):
        # Read DB credentials from environment variables
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')

    def create_connection(self):
        """Create and return a connection to the PostgreSQL database."""
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        
    def setup_database(self):
        """Initialize the PostgreSQL database."""
        try:
            with self.create_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_favorites (
                            username VARCHAR(100) PRIMARY KEY,
                            first_name VARCHAR(100),
                            last_name VARCHAR(100),
                            favorite_sound VARCHAR(100)
                        )
                    """)
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Database setup error: {e}")
    
    def save_favorite_sound(self, username, sound):
        """Save or update the user's favorite sound."""
        try:
            with self.create_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''UPDATE user_favorites SET favorite_sound = %s WHERE username = %s'''
                    cursor.execute(query, (sound, username))
                    conn.commit()
                    print(f"Updated favorite sound for {username} to '{sound}'.")
        except psycopg2.Error as e:
            print(f"Error saving favorite sound: {e}")

    def get_favorite_sound(self, username):
        """Retrieve the user's favorite sound."""
        try:
            with self.create_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''SELECT favorite_sound FROM user_favorites WHERE username = %s'''
                    cursor.execute(query, (username,))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except psycopg2.Error as e:
            print(f"Error retrieving favorite sound: {e}")
            return None

    def get_user(self, username):
        """Retrieve the user info from the database."""
        try:
            with self.create_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''SELECT username, first_name, last_name FROM user_favorites WHERE username = %s'''
                    cursor.execute(query, (username,))
                    result = cursor.fetchone()
                    return result
        except psycopg2.Error as e:
            print(f"Error retrieving user: {e}")
            return None

    def remove_favorite_sound(self, username):
        """Remove a user's favorite sound."""
        try:
            with self.create_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''UPDATE user_favorites SET favorite_sound = NULL WHERE username = %s'''
                    cursor.execute(query, (username,))
                    conn.commit()
                    print(f"Removed favorite sound for {username}.")
        except psycopg2.Error as e:
            print(f"Error removing favorite sound: {e}")

    def create_user(self, username, first_name, last_name):
        """Create a new user in the database."""
        try:
            with self.create_connection() as conn:
                with conn.cursor() as cursor:
                    query = '''INSERT INTO user_favorites (username, first_name, last_name) VALUES (%s, %s, %s)'''
                    cursor.execute(query, (username, first_name, last_name))
                    conn.commit()
                    print(f"Created user: {username} ({first_name} {last_name}).")
        except psycopg2.Error as e:
            print(f"Error creating user: {e}")
