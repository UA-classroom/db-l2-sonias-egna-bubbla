import os

import psycopg2
import db
from db_setup import get_connection
from fastapi import FastAPI, HTTPException, Body

app = FastAPI()

"""
Innehåller endpoints för alla tabeller
"""

# Bid endpoint


@app.get("/bids")
def get_all_bids():
    """Hämtar alla bud"""
    try:
        connection = get_connection()
        bids = db.get_all_bids(connection)
        return {"bids": bids}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/bids/{bid_id}")
def get_bid(bid_id: int):
    """Hämtar ett specifikt bud"""
    try:
        connection = get_connection()
        bid = db.get_bid_by_id(connection, bid_id)
        return bid
    except ValueError:
        raise HTTPException(status_code=404, detail="Bud hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/listings/{listing_id}/bids")
def get_bids_for_listing(listing_id: int):
    """Hämtar alla bud för en annons"""
    try:
        connection = get_connection()
        bids = db.get_bids_for_listing(connection, listing_id)
        return {"bids": bids}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/bids", status_code=201)
def create_bid(
    user_id: int = Body(...), listing_id: int = Body(...), bid_amount: float = Body(...)
):
    """Skapar ett nytt bud"""
    try:
        connection = get_connection()
        new_bid = db.create_bid(connection, user_id, listing_id, bid_amount)
        return new_bid
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa bud")


@app.delete("/bids/{bid_id}")
def delete_bid(bid_id: int):
    """Raderar ett bud"""
    try:
        connection = get_connection()
        result = db.delete_bid(connection, bid_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Bud hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# User_ratings endpoints


@app.get("/user-ratings")
def get_all_user_ratings():
    """Hämtar alla användaromdömmen"""
    try:
        connection = get_connection()
        ratings = db.get_all_user_ratings(connection)
        return {"ratings": ratings}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/users/{user_id}/rating")
def get_user_rating(user_id: int):
    """Hämtar omdöme för en användare"""
    try:
        connection = get_connection()
        rating = db.get_user_rating_by_user_id(connection, user_id)
        return rating
    except ValueError:
        raise HTTPException(status_code=404, detail="Omdöme hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/user-ratings", status_code=201)
def create_user_rating(
    user_id: int = Body(...),
    total_ratings: int = Body(0),
    average_rating: float = Body(0.00),
):
    """Skapar ett nytt omdöme"""
    try:
        connection = get_connection()
        new_rating = db.create_user_rating(
            connection, user_id, total_ratings, average_rating
        )
        return new_rating
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa omdöme")


@app.put("/users/{user_id}/rating")
def update_user_rating(
    user_id: int, total_ratings: int = None, average_rating: float = None
):
    """Uppdaterar ett omdöme"""
    try:
        connection = get_connection()
        updated_rating = db.update_user_rating(
            connection, user_id, total_ratings, average_rating
        )
        return updated_rating
    except ValueError:
        raise HTTPException(status_code=404, detail="Omdöme hittades inte")
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte uppdatera omdöme")


@app.delete("/users/{user_id}/rating")
def delete_user_rating(user_id: int):
    """Raderar ett omdöme"""
    try:
        connection = get_connection()
        result = db.delete_user_rating(connection, user_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Omdöme hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Review endpoints


@app.get("/reviews")
def get_all_reviews():
    """Hämtar alla recensioner"""
    try:
        connection = get_connection()
        reviews = db.get_all_reviews(connection)
        return {"reviews": reviews}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/reviews/{review_id}")
def get_review(review_id: int):
    """Hämtar en recension"""
    try:
        connection = get_connection()
        review = db.get_review_by_id(connection, review_id)
        return review
    except ValueError:
        raise HTTPException(status_code=404, detail="Recension hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/users/{user_id}/reviews")
def get_reviews_for_user(user_id: int):
    """Hämtar recensioner för en användare"""
    try:
        connection = get_connection()
        reviews = db.get_reviews_for_user(connection, user_id)
        return {"reviews": reviews}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/reviews", status_code=201)
def create_review(
    reviewer_id: int = Body(...),
    reviewed_user_id: int = Body(...),
    listing_id: int = Body(...),
    rating: int = Body(...),
    review_text: str = Body(None),
):
    """Skapar en ny recension"""
    try:
        connection = get_connection()
        new_review = db.create_review(
            connection, reviewer_id, reviewed_user_id, listing_id, rating, review_text
        )
        return new_review
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa recension")


@app.delete("/reviews/{review_id}")
def delete_review(review_id: int):
    """Raderar en recension"""
    try:
        connection = get_connection()
        result = db.delete_review(connection, review_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Recension hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Image endpoints
@app.get("/images")
def get_all_images():
    """Hämtar alla bilder"""
    try:
        connection = get_connection()
        images = db.get_all_images(connection)
        return {"images": images}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/images/{image_id}")
def get_image(image_id: int):
    """Hämtar en bild"""
    try:
        connection = get_connection()
        image = db.get_image_by_id(connection, image_id)
        return image
    except ValueError:
        raise HTTPException(status_code=404, detail="Bild hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/listings/{listing_id}/images")
def get_images_for_listing(listing_id: int):
    """Hämtar bilder för en annons"""
    try:
        connection = get_connection()
        images = db.get_images_for_listing(connection, listing_id)
        return {"images": images}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/images", status_code=201)
def create_image(
    user_id: int = Body(...), listing_id: int = Body(...), image_url: str = Body(...)
):
    """Skapar en ny bild"""
    try:
        connection = get_connection()
        new_image = db.create_image(connection, user_id, listing_id, image_url)
        return new_image
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa bild")


@app.delete("/images/{image_id}")
def delete_image(image_id: int):
    """Raderar en bild"""
    try:
        connection = get_connection()
        result = db.delete_image(connection, image_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Bild hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Report endpoints
@app.get("/reports")
def get_all_reports():
    """Hämtar alla rapporteringar"""
    try:
        connection = get_connection()
        reports = db.get_all_reports(connection)
        return {"reports": reports}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/reports/{report_id}")
def get_report(report_id: int):
    """Hämtar en rapport"""
    try:
        connection = get_connection()
        report = db.get_report_by_id(connection, report_id)
        return report
    except ValueError:
        raise HTTPException(status_code=404, detail="Rapport hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/listings/{listing_id}/reports")
def get_reports_for_listing(listing_id: int):
    """Hämtar rapporteringar för en annons"""
    try:
        connection = get_connection()
        reports = db.get_reports_for_listing(connection, listing_id)
        return {"reports": reports}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/reports", status_code=201)
def create_report(
    user_id: int = Body(...),
    listing_id: int = Body(...),
    report_reason: str = Body(...),
):
    """Skapar en ny rapportering"""
    try:
        connection = get_connection()
        new_report = db.create_report(connection, user_id, listing_id, report_reason)
        return new_report
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa rapportering")


@app.delete("/reports/{report_id}")
def delete_report(report_id: int):
    """Raderar en rapportering"""
    try:
        connection = get_connection()
        result = db.delete_report(connection, report_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Rapportering hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# User endpoints


@app.get("/users")
def get_all_users():
    """Hämtar alla användare"""
    try:
        connection = get_connection()
        users = db.get_all_users(connection)
        return {"users": users}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Hämtar en användare"""
    try:
        connection = get_connection()
        user = db.get_user_by_id(connection, user_id)
        return user
    except ValueError:
        raise HTTPException(status_code=404, detail="Användare hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/users", status_code=201)
def create_user(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    user_since: str = Body(...),
    date_of_birth: str = Body(...),
    phone_number: str = Body(None),
):
    """Skapar en ny användare"""
    try:
        connection = get_connection()
        new_user = db.create_user(
            connection,
            username,
            email,
            password,
            user_since,
            date_of_birth,
            phone_number,
        )
        return new_user
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa användare")


@app.put("/users/{user_id}")
def update_user(user_id: int, email: str = None, phone_number: str = None):
    """Uppdaterar en användare"""
    try:
        connection = get_connection()
        updated_user = db.update_user(connection, user_id, email, phone_number)
        return updated_user
    except ValueError:
        raise HTTPException(status_code=404, detail="Användare hittades inte")
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte uppdatera användare")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Raderar en användare"""
    try:
        connection = get_connection()
        result = db.delete_user(connection, user_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Användare hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Category Endpoints


@app.get("/categories")
def get_all_categories():
    """Hämtar alla kategorier"""
    try:
        connection = get_connection()
        categories = db.get_all_categories(connection)
        return {"categories": categories}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/categories", status_code=201)
def create_category(name: str = Body(..., embed=True)):
    """Skapar en ny kategori"""
    try:
        connection = get_connection()
        new_category = db.create_category(connection, name)
        return new_category
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa kategori")


@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    """Raderar en kategori"""
    try:
        connection = get_connection()
        result = db.delete_category(connection, category_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Kategori hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Listing endpoints


@app.get("/listings")
def get_all_listings():
    """Hämtar alla annonser"""
    try:
        connection = get_connection()
        listings = db.get_all_listings(connection)
        return {"listings": listings}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/listings/{listing_id}")
def get_listing(listing_id: int):
    """Hämtar en annons"""
    try:
        connection = get_connection()
        listing = db.get_listing_by_id(connection, listing_id)
        return listing
    except ValueError:
        raise HTTPException(status_code=404, detail="Annons hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/listings", status_code=201)
def create_listing(
    user_id: int = Body(...),
    category_id: int = Body(...),
    title: str = Body(...),
    listing_type: str = Body(...),
    price: float = Body(...),
    region: str = Body(...),
    status: str = Body(...),
    description: str = Body(...),
    image_url: str = Body(None),
):
    """Skapar en ny annons"""
    try:
        connection = get_connection()
        new_listing = db.create_listing(
            connection,
            user_id,
            category_id,
            title,
            listing_type,
            price,
            region,
            status,
            description,
            image_url,
        )
        return new_listing
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa annons")


@app.put("/listings/{listing_id}")
def update_listing(
    listing_id: int,
    category_id: int = None,
    title: str = None,
    listing_type: str = None,
    price: float = None,
    region: str = None,
    status: str = None,
    description: str = None,
    image_url: str = None,
):
    """Uppdaterar en annons"""
    try:
        connection = get_connection()
        updated_listing = db.update_listing(
            connection,
            listing_id,
            category_id,
            title,
            listing_type,
            price,
            region,
            status,
            description,
            image_url,
        )
        return updated_listing
    except ValueError:
        raise HTTPException(status_code=404, detail="Annons hittades inte")
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte uppdatera annons")


@app.delete("/listings/{listing_id}")
def delete_listing(listing_id: int):
    """Raderar en annons"""
    try:
        connection = get_connection()
        result = db.delete_listing(connection, listing_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Annons hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Watch list endpoints


@app.get("/users/{user_id}/watchlist")
def get_watchlist(user_id: int):
    """Hämtar bevakningslista"""
    try:
        connection = get_connection()
        watchlist = db.get_all_watched_listings(connection, user_id)
        return {"watchlist": watchlist}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/watchlist", status_code=201)
def add_to_watchlist(user_id: int = Body(...), listing_id: int = Body(...)):
    """Lägger till i bevakningslista"""
    try:
        connection = get_connection()
        result = db.add_to_watch_list(connection, user_id, listing_id)
        return result
    except Exception as error:
        raise HTTPException(
            status_code=400, detail="Kunde inte lägga till i bevakningslista"
        )


@app.delete("/watchlist")
def remove_from_watchlist(user_id: int, listing_id: int):
    """Tar bort från bevakningslista"""
    try:
        connection = get_connection()
        result = db.remove_from_watch_list(connection, user_id, listing_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Finns inte i bevakningslista")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Message Endpoints


@app.get("/users/{user_id}/messages")
def get_messages(user_id: int):
    """Hämtar meddelanden för en användare"""
    try:
        connection = get_connection()
        messages = db.get_all_messages_for_user(connection, user_id)
        return {"messages": messages}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/messages", status_code=201)
def create_message(
    sender_id: int = Body(...),
    recipient_id: int = Body(...),
    listing_id: int = Body(...),
    message_text: str = Body(...),
):
    """Skapar ett nytt meddelande"""
    try:
        connection = get_connection()
        new_message = db.create_message(
            connection, sender_id, recipient_id, listing_id, message_text
        )
        return new_message
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa meddelande")


@app.put("/messages/{message_id}")
def mark_message_read(message_id: int):
    """Markerar meddelande som läst"""
    try:
        connection = get_connection()
        result = db.mark_message_as_read(connection, message_id)
        return result
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte uppdatera meddelande")


@app.delete("/messages/{message_id}")
def delete_message(message_id: int):
    """Raderar ett meddelande"""
    try:
        connection = get_connection()
        result = db.delete_message(connection, message_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Meddelande hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Transaction Endpoints


@app.get("/transactions")
def get_all_transactions():
    """Hämtar alla transaktioner"""
    try:
        connection = get_connection()
        transactions = db.get_all_transactions(connection)
        return {"transactions": transactions}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    """Hämtar en transaktion"""
    try:
        connection = get_connection()
        transaction = db.get_transaction_by_id(connection, transaction_id)
        return transaction
    except ValueError:
        raise HTTPException(status_code=404, detail="Transaktion hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/users/{user_id}/transactions")
def get_user_transactions(user_id: int):
    """Hämtar transaktioner för en användare"""
    try:
        connection = get_connection()
        transactions = db.get_transactions_by_user_id(connection, user_id)
        return {"transactions": transactions}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/transactions", status_code=201)
def create_transaction(
    user_id: int = Body(...),
    listing_id: int = Body(...),
    amount: float = Body(...),
    status: str = Body(...),
    bid_id: int = Body(None),
):
    """Skapar en ny transaktion"""
    try:
        connection = get_connection()
        new_transaction = db.create_transaction(
            connection, user_id, listing_id, amount, status, bid_id
        )
        return new_transaction
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa transaktion")


@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, new_status: str):
    """Uppdaterar en transaktion"""
    try:
        connection = get_connection()
        updated_transaction = db.update_transaction(
            connection, transaction_id, new_status
        )
        return updated_transaction
    except ValueError:
        raise HTTPException(status_code=404, detail="Transaktion hittades inte")
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte uppdatera transaktion")


# Payment method


@app.get("/payments")
def get_all_payments():
    """Hämtar alla betalningar"""
    try:
        connection = get_connection()
        payments = db.get_all_payments(connection)
        return {"payments": payments}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/transactions/{transaction_id}/payment")
def get_payment(transaction_id: int):
    """Hämtar betalning för en transaktion"""
    try:
        connection = get_connection()
        payment = db.get_payment_by_transaction_id(connection, transaction_id)
        return payment
    except ValueError:
        raise HTTPException(status_code=404, detail="Betalning hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/payments", status_code=201)
def create_payment(
    transaction_id: int = Body(...),
    listing_id: int = Body(...),
    payment_method: str = Body(...),
    payment_status: str = Body(...),
    amount: float = Body(...),
):
    """Skapar en ny betalning"""
    try:
        connection = get_connection()
        new_payment = db.create_payment(
            connection,
            transaction_id,
            listing_id,
            payment_method,
            payment_status,
            amount,
        )
        return new_payment
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa betalning")


@app.put("/payments/{payment_id}")
def update_payment(payment_id: int, new_status: str):
    """Uppdaterar betalningsstatus"""
    try:
        connection = get_connection()
        updated_payment = db.update_payment_status(connection, payment_id, new_status)
        return updated_payment
    except ValueError:
        raise HTTPException(status_code=404, detail="Betalning hittades inte")
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte uppdatera betalning")


# Notification Endpoints
@app.get("/users/{user_id}/notifications")
def get_notifications(user_id: int):
    """Hämtar notiser för en användare"""
    try:
        connection = get_connection()
        notifications = db.get_notifications_by_user_id(connection, user_id)
        return {"notiser": notifications}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.get("/users/{user_id}/notifications/unread")
def get_unread_notifications(user_id: int):
    """Hämtar olästa notiser"""
    try:
        connection = get_connection()
        notifications = db.get_unread_notifications(connection, user_id)
        return {"notiser": notifications}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/notifications", status_code=201)
def create_notification(
    user_id: int = Body(...),
    listing_id: int = Body(...),
    notification_type: str = Body(...),
    notification_message: str = Body(...),
):
    """Skapar en ny notis"""
    try:
        connection = get_connection()
        new_notification = db.create_notification(
            connection, user_id, listing_id, notification_type, notification_message
        )
        return new_notification
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa notis")


@app.put("/users/{user_id}/notifications/mark-read")
def mark_notifications_read(user_id: int):
    """Markerar alla notiser som lästa"""
    try:
        connection = get_connection()
        result = db.mark_all_notifications_as_read(connection, user_id)
        return {"marked": len(result)}
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte uppdatera notiser")


@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int):
    """Raderar en notis"""
    try:
        connection = get_connection()
        result = db.delete_notification(connection, notification_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Notis hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Listing comment endpoints


@app.get("/listings/{listing_id}/comments")
def get_listing_comments(listing_id: int):
    """Hämtar kommentarer för en annons"""
    try:
        connection = get_connection()
        comments = db.get_comments_by_listing_id(connection, listing_id)
        return {"comments": comments}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/comments", status_code=201)
def create_comment(
    user_id: int = Body(...), listing_id: int = Body(...), comment_text: str = Body(...)
):
    """Skapar en ny kommentar"""
    try:
        connection = get_connection()
        new_comment = db.create_listing_comment(
            connection, user_id, listing_id, comment_text
        )
        return new_comment
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa kommentar")


@app.put("/comments/{comment_id}/answer")
def answer_listing_comment(comment_id: int, answer_text: str):
    """Svarar på en kommentar"""
    try:
        connection = get_connection()
        answered_comment = db.answer_comment(connection, comment_id, answer_text)
        return answered_comment
    except ValueError:
        raise HTTPException(status_code=404, detail="Kommentar hittades inte")
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte svara på kommentar")


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    """Raderar en kommentar"""
    try:
        connection = get_connection()
        result = db.delete_listing_comment(connection, comment_id)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Kommentar hittades inte")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


# Shipping Endpoints


@app.get("/listings/{listing_id}/shipping")
def get_shipping(listing_id: int):
    """Hämtar fraktdetaljer för en annons"""
    try:
        connection = get_connection()
        shipping = db.get_shipping_by_listing_id(connection, listing_id)
        return shipping
    except Exception as error:
        raise HTTPException(status_code=500, detail="Något gick fel")


@app.post("/shipping", status_code=201)
def create_shipping(
    user_id: int = Body(...),
    listing_id: int = Body(...),
    shipping_method: str = Body(...),
    shipping_cost: float = Body(...),
    estimated_delivery_days: int = Body(None),
    tracking_number: str = Body(None),
    status: str = Body(None),
    shipped_at: str = Body(None),
):
    """Skapar fraktdetaljer"""
    try:
        connection = get_connection()
        new_shipping = db.create_shipping_details(
            connection,
            user_id,
            listing_id,
            shipping_method,
            shipping_cost,
            estimated_delivery_days,
            tracking_number,
            status,
            shipped_at,
        )
        return new_shipping
    except Exception as error:
        raise HTTPException(status_code=400, detail="Kunde inte skapa fraktdetaljer")


@app.put("/shipping/{shipping_id}")
def update_shipping(
    shipping_id: int, tracking_number: str, status: str, shipped_at: str = None
):
    """Uppdaterar fraktdetaljer"""
    try:
        connection = get_connection()
        updated_shipping = db.update_shipping_tracking(
            connection, shipping_id, tracking_number, status, shipped_at
        )
        return updated_shipping
    except ValueError:
        raise HTTPException(status_code=404, detail="Fraktdetaljer hittades inte")
    except Exception as error:
        raise HTTPException(
            status_code=400, detail="Kunde inte uppdatera fraktdetaljer"
        )


# Root Endpoint


@app.get("/")
def root():
    """Välkomstmeddelande"""
    return {"message": "Välkommen"}
