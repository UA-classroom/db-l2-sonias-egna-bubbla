import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
# Koppling till databas
DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


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
    Creates all 15 tables for Tradera application
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Tabell 1: Users (Användare)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY NOT NULL,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                user_since TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                date_of_birth DATE NOT NULL,
                phone_number VARCHAR(20)
            )
        """
        )

        # Tabell 2: Categories (Kategorier)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            )
        """
        )

        # Tabell 3: Listings (Annonser)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS listings (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                category_id BIGINT NOT NULL,
                title VARCHAR(100) NOT NULL,
                image_url VARCHAR(500),
                listing_type VARCHAR(255) NOT NULL CHECK (listing_type IN ('buying', 'selling', 'free')),
                price DECIMAL(10, 2) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                region VARCHAR(255) NOT NULL,
                status VARCHAR(255) NOT NULL CHECK (status IN ('active', 'sold', 'closed')),
                description TEXT NOT NULL
            )
        """
        )

        # Tabell 4: Listings_Watch_List (Bevakningslista)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS listings_watch_list (
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, listing_id)
            )
        """
        )

        # Tabell 5: Messages (Meddelanden)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id BIGSERIAL PRIMARY KEY,
                sender_id BIGINT NOT NULL,
                recipient_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                message_text TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE
            )
        """
        )

        # Tabell 6: Bids (Bud)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bids (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                bid_amount DECIMAL(10,2) NOT NULL
            )
        """
        )

        # Tabell 7: Transactions (Transaktioner)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                bid_id BIGINT,
                listing_id BIGINT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) NOT NULL,
                amount DECIMAL(10,2) NOT NULL
            )
        """
        )

        # Tabell 8: Payments (Betalningar)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id BIGSERIAL PRIMARY KEY,
                transaction_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                payment_method VARCHAR(50) NOT NULL,
                payment_status VARCHAR(50) NOT NULL CHECK (payment_status IN ('pending', 'completed', 'failed', 'cancelled', 'refunded')),
                amount DECIMAL(10, 2) NOT NULL,
                paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Tabell 9: User_Ratings (Användarens totala betyg)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_ratings (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                total_ratings INT NOT NULL DEFAULT 0,
                average_rating DECIMAL(3,2) NOT NULL DEFAULT 0.00
            )
        """
        )

        # Tabell 10: Reviews (Recensioner)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews (
                id BIGSERIAL PRIMARY KEY,
                reviewer_id BIGINT NOT NULL,
                reviewed_user_id BIGINT NOT NULL,
                listing_id BIGINT,
                rating INT NOT NULL,
                review_text TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Tabell 11: Images (Bilder på annonser)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS images (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                image_url VARCHAR(500) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Tabell 12: Notifications (Notifieringar)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notifications (
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                notification_type VARCHAR(50) NOT NULL,
                notification_message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP NOT NULL
            )
        """
        )

        # Tabell 13: Listing_Comments (Kommentarer på annonser)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS listing_comments (
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                comment_text TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                answer_text TEXT,
                answered_at TIMESTAMP
            )
        """
        )

        # Tabell 14: Shipping_Details (Fraktdetaljer)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS shipping_details (
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                shipping_method VARCHAR(100) NOT NULL,
                shipping_cost DECIMAL(10,2) NOT NULL,
                estimated_delivery_days INT,
                tracking_number VARCHAR(100),
                status VARCHAR(50),
                shipped_at TIMESTAMP
            )
        """
        )

        # Tabell 15: Reports (Rapporterade annonser)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                listing_id BIGINT NOT NULL,
                report_reason TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Spara allt
        connection.commit()

    except psycopg2.Error as error:
        connection.rollback()
        print(f"Error creating tables: {error}")
        raise
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
