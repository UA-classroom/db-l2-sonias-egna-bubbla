import os
import psycopg2 
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("tradera_db")
PASSWORD = os.getenv("ditt_lösenord_här")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )


def create_tables():
    """
    A function to create the necessary tables for the project.
    Creates: Bids, User_Ratings, Reviews, Images, Reports
    """
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Tabell 1 Bids (bud) 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bids (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                bid_amount DECIMAL(10,2) NOT NULL
            )
        """)

        # Tabell 2: User_Ratings (Användarens totala betyg)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_ratings (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                total_ratings INT NOT NULL DEFAULT 0,
                average_rating DECIMAL(3,2) NOT NULL DEFAULT 0.00
            )
        """)

        # Tabell 3: Reviews (Recensioner)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id BIGSERIAL PRIMARY KEY,
                reviewer_id BIGINT NOT NULL,
                reviewed_user_id BIGINT NOT NULL,
                listing_id BIGINT,
                rating INT NOT NULL,
                review_text TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabell 4: Reports (Rapporterade annonser)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                report_reason TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)



if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
