import psycopg2
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""


# Bid functions


def get_all_bids(connection):
    """Hämtar alla bud från databasen"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM bids ORDER BY created_at DESC")
            bids = cursor.fetchall()
    return bids


def get_bid_by_id(connection, bid_id):
    """Hämtar ett specifikt bud"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM bids WHERE id = %s", (bid_id,))
            bid = cursor.fetchone()

    if not bid:
        raise ValueError(f"Bud med id {bid_id} finns inte")

    return bid


def get_bids_for_listing(connection, listing_id):
    """Hämtar alla bud för en specifik annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM bids 
                WHERE listing_id = %s 
                ORDER BY bid_amount DESC
            """,
                (listing_id,),
            )
            bids = cursor.fetchall()
    return bids


def create_bid(connection, user_id, listing_id, bid_amount):
    """Skapar ett nytt bud"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO bids (user_id, listing_id, bid_amount)
                VALUES (%s, %s, %s)
                RETURNING *
            """,
                (user_id, listing_id, bid_amount),
            )
            new_bid = cursor.fetchone()
    return new_bid


def delete_bid(connection, bid_id):
    """Raderar ett bud"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM bids WHERE id = %s RETURNING id", (bid_id,))
            deleted_bid = cursor.fetchone()

    if not deleted_bid:
        raise ValueError(f"Bud med id {bid_id} finns inte")

    return {"message": "Bud raderat", "id": deleted_bid["id"]}


# User_Ratings functions


def get_all_user_ratings(connection):
    """Hämtar alla användarratings"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM user_ratings")
            ratings = cursor.fetchall()
    return ratings


def get_user_rating_by_user_id(connection, user_id):
    """Hämtar rating för en specifik användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM user_ratings WHERE user_id = %s", (user_id,))
            rating = cursor.fetchone()

    if not rating:
        raise ValueError(f"Rating för användare {user_id} finns inte")

    return rating


def create_user_rating(connection, user_id, total_ratings=0, average_rating=0.00):
    """Skapar ett nytt användarrating"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO user_ratings (user_id, total_ratings, average_rating)
                VALUES (%s, %s, %s)
                RETURNING *
            """,
                (user_id, total_ratings, average_rating),
            )
            new_rating = cursor.fetchone()
    return new_rating


def update_user_rating(connection, user_id, total_ratings=None, average_rating=None):
    """Uppdaterar ett användarrating"""
    updates = []
    values = []

    if total_ratings is not None:
        updates.append("total_ratings = %s")
        values.append(total_ratings)
    if average_rating is not None:
        updates.append("average_rating = %s")
        values.append(average_rating)

    if not updates:
        raise ValueError("Inget att uppdatera")

    values.append(user_id)
    query = (
        f"UPDATE user_ratings SET {', '.join(updates)} WHERE user_id = %s RETURNING *"
    )

    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, values)
            updated_rating = cursor.fetchone()

    if not updated_rating:
        raise ValueError(f"Rating för användare {user_id} finns inte")

    return updated_rating


def delete_user_rating(connection, user_id):
    """Raderar ett användarrating"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM user_ratings WHERE user_id = %s RETURNING id", (user_id,)
            )
            deleted_rating = cursor.fetchone()

    if not deleted_rating:
        raise ValueError(f"Rating för användare {user_id} finns inte")

    return {"message": "Rating raderat", "id": deleted_rating["id"]}


# Review Functions


def get_all_reviews(conncection):
    """Hämtar alla recenssioner"""
    with conncection:
        with conncection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM reviews ORDER BY created_at DESC")
            reviews = cursor.fetchall()
    return reviews


def get_review_by_id(connection, review_id):
    """Hämtar en specifik recension"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM reviews WHERE id = %s", (review_id,))
            review = cursor.fetchone()

    if not review:
        raise ValueError(f"Recension med id {review_id} finns inte")

    return review


def get_reviews_for_user(connection, user_id):
    """Hämtar alla recensioner för en användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM reviews 
                WHERE reviewed_user_id = %s 
                ORDER BY created_at DESC
            """,
                (user_id,),
            )
            reviews = cursor.fetchall()
    return reviews


def create_review(
    connection, reviewer_id, reviewed_user_id, listing_id, rating, review_text=None
):
    """Skapar en ny recension"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO reviews (reviewer_id, reviewed_user_id, listing_id, rating, review_text)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            """,
                (reviewer_id, reviewed_user_id, listing_id, rating, review_text),
            )
            new_review = cursor.fetchone()
    return new_review


def delete_review(connection, review_id):
    """Raderar en recension"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM reviews WHERE id = %s RETURNING id", (review_id,)
            )
            deleted_review = cursor.fetchone()

    if not deleted_review:
        raise ValueError(f"Recension med id {review_id} finns inte")

    return {"message": "Recension raderad", "id": deleted_review["id"]}


# Image Function


def get_all_images(connection):
    """Hämtar alla bilder"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM images ORDER BY created_at DESC")
            images = cursor.fetchall()
    return images


def get_image_by_id(connection, image_id):
    """Hämtar en specifik bild"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM images WHERE id = %s", (image_id,))
            image = cursor.fetchone()

    if not image:
        raise ValueError(f"Bild med id {image_id} finns inte")

    return image


def get_images_for_listing(connection, listing_id):
    """Hämtar alla bilder för en annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM images 
                WHERE listing_id = %s 
                ORDER BY created_at ASC
            """,
                (listing_id,),
            )
            images = cursor.fetchall()
    return images


def create_image(connection, user_id, listing_id, image_url):
    """Lägger till en ny bild"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO images (user_id, listing_id, image_url)
                VALUES (%s, %s, %s)
                RETURNING *
            """,
                (user_id, listing_id, image_url),
            )
            new_image = cursor.fetchone()
    return new_image


def delete_image(connection, image_id):
    """Raderar en bild"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM images WHERE id = %s RETURNING id", (image_id,))
            deleted_image = cursor.fetchone()

    if not deleted_image:
        raise ValueError(f"Bild med id {image_id} finns inte")

    return {"message": "Bild raderad", "id": deleted_image["id"]}


# Report functions


def get_all_reports(connection):
    """Hämtar alla rapporteringar"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
            reports = cursor.fetchall()
    return reports


def get_report_by_id(connection, report_id):
    """Hämtar en specifik rapport"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM reports WHERE id = %s", (report_id,))
            report = cursor.fetchone()

    if not report:
        raise ValueError(f"Rapport med id {report_id} finns inte")

    return report


def get_reports_for_listing(connection, listing_id):
    """Hämtar alla rapporter för en annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM reports 
                WHERE listing_id = %s 
                ORDER BY created_at DESC
            """,
                (listing_id,),
            )
            reports = cursor.fetchall()
    return reports


def create_report(connection, user_id, listing_id, report_reason):
    """Skapar en ny rapportering"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO reports (user_id, listing_id, report_reason)
                VALUES (%s, %s, %s)
                RETURNING *
            """,
                (user_id, listing_id, report_reason),
            )
            new_report = cursor.fetchone()
    return new_report


def delete_report(connection, report_id):
    """Raderar en rapportering"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM reports WHERE id = %s RETURNING id", (report_id,)
            )
            deleted_report = cursor.fetchone()

    if not deleted_report:
        raise ValueError(f"Rapport med id {report_id} finns inte")

    return {"message": "Rapportering raderad", "id": deleted_report["id"]}


# User function
def get_all_users(connection):
    """Hämtar alla användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM users")
            all_users = cursor.fetchall()
    return all_users


def get_user_by_id(connection, user_id):
    """Hämtar en specifik användare med ID"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, username, email, user_since, date_of_birth, phone_number 
                FROM users 
                WHERE id = %s
            """,
                (user_id,),
            )
            user = cursor.fetchone()

    if not user:
        raise ValueError(f"Användare med id {user_id} finns inte")

    return user


def get_user_by_email(connection, email):
    """Hämtar användare med email (för inloggning)"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, username, email, user_since, date_of_birth, phone_number 
                FROM users 
                WHERE email = %s
            """,
                (email,),
            )
            user = cursor.fetchone()
    return user


def get_user_by_username(connection, username):
    """Hämtar användare med username (för inloggning)"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, username, email, user_since, date_of_birth, phone_number 
                FROM users 
                WHERE username = %s
            """,
                (username,),
            )
            user = cursor.fetchone()
    return user


def create_user(
    connection, username, email, password, user_since, date_of_birth, phone_number
):
    """Skapar en ny användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, email, password, user_since, date_of_birth, phone_number) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                RETURNING *
            """,
                (username, email, password, user_since, date_of_birth, phone_number),
            )
            new_user = cursor.fetchone()
    return new_user


def update_user(connection, user_id, email=None, phone_number=None):
    """Uppdaterar en specifik användares email eller telefonnummer"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE users 
                SET email = COALESCE(%s, email),
                    phone_number = COALESCE(%s, phone_number)
                WHERE id = %s 
                RETURNING *
            """,
                (email, phone_number, user_id),
            )
            updated_user = cursor.fetchone()

    if not updated_user:
        raise ValueError(f"Användare med id {user_id} finns inte")

    return updated_user


def delete_user(connection, user_id):
    """Raderar en användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s RETURNING *", (user_id,))
            deleted_user = cursor.fetchone()

    if not deleted_user:
        raise ValueError(f"Användare med id {user_id} finns inte")

    return {"message": "Användare raderad", "user": deleted_user}


# Category Funcition
def get_all_categories(connection):
    """Hämtar alla kategorier"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()
    return categories


def create_category(connection, name):
    """Skapar en ny kategori"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO categories (name) 
                VALUES (%s) 
                RETURNING *
            """,
                (name,),
            )
            new_category = cursor.fetchone()
    return new_category


def delete_category(connection, category_id):
    """Raderar en kategori"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM categories WHERE id = %s RETURNING *", (category_id,)
            )
            deleted_category = cursor.fetchone()

    if not deleted_category:
        raise ValueError(f"Kategori med id {category_id} finns inte")

    return {"message": "Kategori raderad", "id": deleted_category["id"]}


# Listing function
def get_all_listings(connection):
    """Hämtar alla annonser"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM listings ORDER BY created_at DESC")
            listings = cursor.fetchall()
    return listings


def get_listing_by_id(connection, listing_id):
    """Hämtar en specifik annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM listings WHERE id = %s", (listing_id,))
            listing = cursor.fetchone()

    if not listing:
        raise ValueError(f"Annons med id {listing_id} finns inte")

    return listing


def create_listing(
    connection,
    user_id,
    category_id,
    title,
    listing_type,
    price,
    region,
    status,
    description,
    image_url=None,
):
    """Skapar en ny annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO listings 
                (user_id, category_id, title, listing_type, price, region, status, description, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING *
            """,
                (
                    user_id,
                    category_id,
                    title,
                    listing_type,
                    price,
                    region,
                    status,
                    description,
                    image_url,
                ),
            )
            new_listing = cursor.fetchone()
    return new_listing


def update_listing(
    connection,
    listing_id,
    category_id=None,
    title=None,
    listing_type=None,
    price=None,
    region=None,
    status=None,
    description=None,
    image_url=None,
):
    """Uppdaterar en annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE listings SET
                category_id = COALESCE(%s, category_id),
                title = COALESCE(%s, title),
                listing_type = COALESCE(%s, listing_type),
                price = COALESCE(%s, price),
                region = COALESCE(%s, region),
                status = COALESCE(%s, status),
                description = COALESCE(%s, description),
                image_url = COALESCE(%s, image_url)
                WHERE id = %s 
                RETURNING *
            """,
                (
                    category_id,
                    title,
                    listing_type,
                    price,
                    region,
                    status,
                    description,
                    image_url,
                    listing_id,
                ),
            )
            updated_listing = cursor.fetchone()

    if not updated_listing:
        raise ValueError(f"Annons med id {listing_id} finns inte")

    return updated_listing


def delete_listing(connection, listing_id):
    """Raderar en annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM listings WHERE id = %s RETURNING *", (listing_id,)
            )
            deleted_listing = cursor.fetchone()

    if not deleted_listing:
        raise ValueError(f"Annons med id {listing_id} finns inte")

    return {"message": "Annons raderad", "id": deleted_listing["id"]}


# Listings Watch list function
def get_all_watched_listings(connection, user_id):
    """Hämtar alla bevakade annonser för en användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM listings_watch_list 
                WHERE user_id = %s
            """,
                (user_id,),
            )
            watched_listings = cursor.fetchall()
    return watched_listings


def add_to_watch_list(connection, user_id, listing_id):
    """Lägger till annons i bevakningslista"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO listings_watch_list (user_id, listing_id)
                VALUES (%s, %s) 
                RETURNING *
            """,
                (user_id, listing_id),
            )
            new_watch = cursor.fetchone()
    return new_watch


def remove_from_watch_list(connection, user_id, listing_id):
    """Tar bort annons från bevakningslista"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE FROM listings_watch_list 
                WHERE user_id = %s AND listing_id = %s 
                RETURNING *
            """,
                (user_id, listing_id),
            )
            deleted_watch = cursor.fetchone()

    if not deleted_watch:
        raise ValueError("Annons fanns inte i bevakningslistan")

    return {"message": "Annons borttagen från bevakningslista"}


# Message function
def get_all_messages_for_user(connection, user_id):
    """Hämtar alla meddelanden för en användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM messages 
                WHERE sender_id = %s OR recipient_id = %s 
                ORDER BY created_at DESC
            """,
                (user_id, user_id),
            )
            messages = cursor.fetchall()
    return messages


def get_conversation(connection, user1_id, user2_id):
    """Hämtar konversation mellan två användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM messages 
                WHERE (sender_id = %s AND recipient_id = %s) 
                   OR (sender_id = %s AND recipient_id = %s)
                ORDER BY created_at ASC
            """,
                (user1_id, user2_id, user2_id, user1_id),
            )
            conversation = cursor.fetchall()
    return conversation


def create_message(connection, sender_id, recipient_id, listing_id, message_text):
    """Skapar ett nytt meddelande"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO messages (sender_id, recipient_id, listing_id, message_text)
                VALUES (%s, %s, %s, %s) 
                RETURNING *
            """,
                (sender_id, recipient_id, listing_id, message_text),
            )
            new_message = cursor.fetchone()
    return new_message


def mark_message_as_read(connection, message_id):
    """Markerar ett meddelande som läst"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE messages 
                SET is_read = TRUE 
                WHERE id = %s 
                RETURNING *
            """,
                (message_id,),
            )
            updated_message = cursor.fetchone()
    return updated_message


def delete_message(connection, message_id):
    """Raderar ett meddelande"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM messages WHERE id = %s RETURNING *", (message_id,)
            )
            deleted_message = cursor.fetchone()

    if not deleted_message:
        raise ValueError(f"Meddelande med id {message_id} finns inte")

    return {"message": "Meddelande raderat", "id": deleted_message["id"]}


# Transaction function
def get_all_transactions(connection):
    """Hämtar alla transaktioner"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM transactions")
            transactions = cursor.fetchall()
    return transactions


def get_transaction_by_id(connection, transaction_id):
    """Hämtar en specifik transaktion"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM transactions WHERE id = %s", (transaction_id,)
            )
            transaction = cursor.fetchone()

    if not transaction:
        raise ValueError(f"Transaktion med id {transaction_id} finns inte")

    return transaction


def get_transactions_by_user_id(connection, user_id):
    """Hämtar alla transaktioner för en användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, user_id, bid_id, listing_id, status, amount
                FROM transactions 
                WHERE user_id = %s
            """,
                (user_id,),
            )
            transactions = cursor.fetchall()
    return transactions


def create_transaction(connection, user_id, listing_id, amount, status, bid_id=None):
    """Skapar en ny transaktion"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO transactions (user_id, listing_id, amount, status, bid_id) 
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING *
            """,
                (user_id, listing_id, amount, status, bid_id),
            )
            new_transaction = cursor.fetchone()
    return new_transaction


def update_transaction(connection, transaction_id, new_status):
    """Uppdaterar status på en transaktion"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE transactions 
                SET status = COALESCE(%s, status)
                WHERE id = %s 
                RETURNING *
            """,
                (new_status, transaction_id),
            )
            updated_transaction = cursor.fetchone()

    if not updated_transaction:
        raise ValueError(f"Transaktion med id {transaction_id} finns inte")

    return updated_transaction


# Payment function


def get_all_payments(connection):
    """Hämtar alla betalningar"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM payments ORDER BY paid_at DESC")
            payments = cursor.fetchall()
    return payments


def get_payment_by_transaction_id(connection, transaction_id):
    """Hämtar betalning för en transaktion"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM payments WHERE transaction_id = %s", (transaction_id,)
            )
            payment = cursor.fetchone()

    if not payment:
        raise ValueError(f"Betalning för transaktion {transaction_id} finns inte")

    return payment


def create_payment(
    connection, transaction_id, listing_id, payment_method, payment_status, amount
):
    """Skapar en ny betalning"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO payments (transaction_id, listing_id, payment_method, payment_status, amount)
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING *
            """,
                (transaction_id, listing_id, payment_method, payment_status, amount),
            )
            new_payment = cursor.fetchone()
    return new_payment


def update_payment_status(connection, payment_id, new_status):
    """Uppdaterar betalningsstatus"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE payments 
                SET payment_status = %s 
                WHERE id = %s 
                RETURNING *
            """,
                (new_status, payment_id),
            )
            updated_payment = cursor.fetchone()

    if not updated_payment:
        raise ValueError(f"Betalning med id {payment_id} finns inte")

    return updated_payment


# Notification function


def get_notifications_by_user_id(connection, user_id):
    """Hämtar alla notifieringar för en användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM notifications WHERE user_id = %s", (user_id,))
            notifications = cursor.fetchall()
    return notifications


def get_unread_notifications(connection, user_id):
    """Hämtar olästa notifieringar för en användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM notifications
                WHERE user_id = %s AND is_read = FALSE
            """,
                (user_id,),
            )
            unread_notifications = cursor.fetchall()
    return unread_notifications


def create_notification(
    connection, user_id, listing_id, notification_type, notification_message
):
    """Skapar en ny notifiering"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO notifications (user_id, listing_id, notification_type, notification_message) 
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """,
                (user_id, listing_id, notification_type, notification_message),
            )
            new_notification = cursor.fetchone()
    return new_notification


def mark_all_notifications_as_read(connection, user_id):
    """Markerar alla notifieringar som lästa"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE notifications
                SET is_read = TRUE 
                WHERE user_id = %s 
                RETURNING *
            """,
                (user_id,),
            )
            marked_notifications = cursor.fetchall()
    return marked_notifications


def delete_notification(connection, notification_id):
    """Raderar en notifiering"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM notifications WHERE id = %s RETURNING *",
                (notification_id,),
            )
            deleted_notification = cursor.fetchone()

    if not deleted_notification:
        raise ValueError(f"Notifiering med id {notification_id} finns inte")

    return {"message": "Notifiering raderad", "id": deleted_notification["id"]}


# Listning_comments function
def get_comments_by_listing_id(connection, listing_id):
    """Hämtar alla kommentarer för en annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, user_id, listing_id, comment_text, answer_text
                FROM listing_comments
                WHERE listing_id = %s
            """,
                (listing_id,),
            )
            comments = cursor.fetchall()
    return comments


def get_comments_by_user_id(connection, user_id):
    """Hämtar alla kommentarer från en användare"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM listing_comments WHERE user_id = %s", (user_id,)
            )
            comments = cursor.fetchall()
    return comments


def create_listing_comment(connection, user_id, listing_id, comment_text):
    """Skapar en ny kommentar"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO listing_comments (user_id, listing_id, comment_text) 
                VALUES (%s, %s, %s)
                RETURNING *
            """,
                (user_id, listing_id, comment_text),
            )
            new_comment = cursor.fetchone()
    return new_comment


def answer_comment(connection, comment_id, answer_text):
    """Svarar på en kommentar"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE listing_comments 
                SET answer_text = %s, answered_at = CURRENT_TIMESTAMP
                WHERE id = %s 
                RETURNING *
            """,
                (answer_text, comment_id),
            )
            answered_comment = cursor.fetchone()

    if not answered_comment:
        raise ValueError(f"Kommentar med id {comment_id} finns inte")

    return answered_comment


def delete_listing_comment(connection, comment_id):
    """Raderar en kommentar"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "DELETE FROM listing_comments WHERE id = %s RETURNING *", (comment_id,)
            )
            deleted_comment = cursor.fetchone()

    if not deleted_comment:
        raise ValueError(f"Kommentar med id {comment_id} finns inte")

    return {"message": "Kommentar raderad", "id": deleted_comment["id"]}


# Shipping_details functions


def get_shipping_by_listing_id(connection, listing_id):
    """Hämtar fraktdetaljer för en annons"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, listing_id, shipping_method, shipping_cost, estimated_delivery_days, tracking_number, status, shipped_at
                FROM shipping_details 
                WHERE listing_id = %s
            """,
                (listing_id,),
            )
            shipping = cursor.fetchone()
    return shipping


def create_shipping_details(
    connection,
    user_id,
    listing_id,
    shipping_method,
    shipping_cost,
    estimated_delivery_days=None,
    tracking_number=None,
    status=None,
    shipped_at=None,
):
    """Skapar fraktdetaljer"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO shipping_details (user_id, listing_id, shipping_method, shipping_cost, estimated_delivery_days, tracking_number, status, shipped_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """,
                (
                    user_id,
                    listing_id,
                    shipping_method,
                    shipping_cost,
                    estimated_delivery_days,
                    tracking_number,
                    status,
                    shipped_at,
                ),
            )
            new_shipping = cursor.fetchone()
    return new_shipping


def update_shipping_tracking(
    connection, shipping_id, tracking_number, status, shipped_at=None
):
    """Uppdaterar spårningsinformation"""
    with connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE shipping_details 
                SET tracking_number = COALESCE(%s, tracking_number),
                    shipped_at = COALESCE(%s, shipped_at),
                    status = COALESCE(%s, status)
                WHERE id = %s 
                RETURNING *
            """,
                (tracking_number, shipped_at, status, shipping_id),
            )
            updated_shipping = cursor.fetchone()

    if not updated_shipping:
        raise ValueError(f"Fraktdetaljer med id {shipping_id} finns inte")

    return updated_shipping


### THIS IS JUST AN EXAMPLE OF A FUNCTION FOR INSPIRATION FOR A LIST-OPERATION (FETCHING MANY ENTRIES)
# def get_items(con):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("SELECT * FROM items;")
#             items = cursor.fetchall()
#     return items


### THIS IS JUST INSPIRATION FOR A DETAIL OPERATION (FETCHING ONE ENTRY)
# def get_item(con, item_id):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("""SELECT * FROM items WHERE id = %s""", (item_id,))
#             item = cursor.fetchone()
#             return item


### THIS IS JUST INSPIRATION FOR A CREATE-OPERATION
# def add_item(con, title, description):
#     with con:
#         with con.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "INSERT INTO items (title, description) VALUES (%s, %s) RETURNING id;",
#                 (title, description),
#             )
#             item_id = cursor.fetchone()["id"]
#     return item_id
