import os
import sys

# Root directory to sys.path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from DB.database import SessionLocal
from DB.models import Collection, CollectionItem, Comment, Like, Publication, SearchHistory, User

def verify_db():
    db = SessionLocal()
    try:
        user = User(
            username="test_user",
            email="test@example.com",
            password_hash="hash123",
            stars=4.5,
        )
        db.add(user)
        db.flush()

        publication = Publication(
            user_id=user.id,
            title="First publication",
            body="Hello from ERD schema",
            image_meta={"width": 1200, "height": 800},
        )
        db.add(publication)
        db.flush()

        collection = Collection(user_id=user.id, name="Favorites")
        db.add(collection)
        db.flush()

        db.add(CollectionItem(collection_id=collection.id, publication_id=publication.id))
        db.add(Like(user_id=user.id, publication_id=publication.id))
        db.add(Comment(post_id=publication.id, user_id=user.id, content="Great post"))
        db.add(SearchHistory(user_id=user.id, query="italian architecture"))
        db.commit()
        db.refresh(user)
        print(f"Created user: {user.username} with ID: {user.id}")

        loaded_user = db.query(User).filter(User.username == "test_user").first()
        loaded_publications = db.query(Publication).filter(Publication.user_id == user.id).count()
        loaded_likes = db.query(Like).filter(Like.user_id == user.id).count()
        loaded_comments = db.query(Comment).filter(Comment.user_id == user.id).count()

        if loaded_user:
            print(f"Verified user: {loaded_user.username} (Email: {loaded_user.email})")
            print(
                f"Related rows -> publications: {loaded_publications}, likes: {loaded_likes}, comments: {loaded_comments}"
            )

        db.delete(loaded_user)
        db.commit()
        print("Cleaned up database.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    verify_db()
