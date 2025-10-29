# app/routes/word_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import random
from app.models.word import Word, UserActivity


def fetch_spell_mastery_words(db: Session, grade_level: str = None):
    from datetime import datetime, timedelta
    from app.models import Word, UserActivity

    # Date ranges
    now = datetime.utcnow()
    ten_days_ago = now - timedelta(days=10)
    seven_days_ago = now - timedelta(days=7)

    # Get all user activities
    user_activities = db.query(UserActivity).all()

    # Group by word_id
    activity_by_word = {}
    for a in user_activities:
        activity_by_word.setdefault(a.word_id, []).append(a)

    # --- Misspelled words in the last 10 days ---
    misspelled_words = [
        wid
        for wid, acts in activity_by_word.items()
        if any(
            not a.is_correct and a.timestamp and a.timestamp >= ten_days_ago
            for a in acts
        )
    ]

    # --- Words spelled correctly but not recently (7 days ago or earlier) ---
    correct_old_words = [
        wid
        for wid, acts in activity_by_word.items()
        if any(a.is_correct and a.timestamp and a.timestamp <= seven_days_ago for a in acts)
    ]

    # Combine both lists, remove duplicates
    selected_word_ids = list(set(misspelled_words + correct_old_words))

    query = db.query(Word)
    if grade_level:
        query = query.filter(Word.grade_level == grade_level)

    if selected_word_ids:
        query = query.filter(Word.id.in_(selected_word_ids))

    words_selected = query.all()
    return words_selected
