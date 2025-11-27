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
