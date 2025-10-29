# app/routes/word_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import random
from app.models.word import Word, UserActivity

def fetch_spell_mastery_words(db: Session, grade_level: str = None, total_words: int = 25):
    """
    Fetch words for Spell Bee Mastery based on user activities and grade filter.
    """

    now = datetime.now(timezone.utc)
    #ten_days_ago = now - timedelta(days=10)
    #one_week_ago = now - timedelta(weeks=1)
    ten_days_ago = datetime.now(timezone.utc) - timedelta(days=10)
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    # Base query for all words
    query = db.query(Word)
    if grade_level:
        query = query.filter(Word.grade_level == grade_level)
    all_words = query.all()

    # Fetch user activities
    activities = db.query(UserActivity).all()

    # Organize activities by word_id
    word_history = {}
    for act in activities:
        if act.word_id not in word_history:
            word_history[act.word_id] = []
        word_history[act.word_id].append(act)

    # Misspelled in last 10 days
    misspelled_words = [
        db.query(Word).get(word_id)
        for word_id, acts in word_history.items()
        if any(not a.is_correct and a.timestamp >= ten_days_ago for a in acts)
    ]

    # Correctly spelled before 1 week
    correct_old_words = [
    w for w, acts in word_history.items()
    if any(a.is_correct and a.timestamp and a.timestamp <= seven_days_ago for a in acts)]
    
    #correct_old_words = [
    #    db.query(Word).get(word_id)
    #    for word_id, acts in word_history.items()
    #    if any(a.is_correct and a.timestamp <= seven_days_ago for a in acts)
    #]

    # Never spelled words
    attempted_word_ids = {a.word_id for a in activities}
    never_spelled_words = [w for w in all_words if w.id not in attempted_word_ids]

    selected_words = []

    # Step 1: 10 random misspelled
    selected_words += random.sample(misspelled_words, min(len(misspelled_words), 10))

    # Step 2: 5 random correct old words
    selected_words += random.sample(correct_old_words, min(len(correct_old_words), 5))

    # Step 3: 10 random never spelled
    selected_words += random.sample(never_spelled_words, min(len(never_spelled_words), 10))

    # Step 4: Fallback
    if len(selected_words) < total_words:
        remaining_words = list(set(all_words) - set(selected_words))
        random.shuffle(remaining_words)
        selected_words += remaining_words[:total_words - len(selected_words)]

    # Limit total and shuffle
    selected_words = selected_words[:total_words]
    random.shuffle(selected_words)

    return selected_words
