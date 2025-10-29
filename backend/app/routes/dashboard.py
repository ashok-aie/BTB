from sqlalchemy.orm import Session
from sqlalchemy import func, case, distinct
from app.models import UserActivity, Word
from datetime import datetime, timedelta

def calculate_failed_dates(streak_dates, start_from="2025-08-01"):
    """Compute failed (non-streak) dates from start_from up to yesterday."""
    today = datetime.now().date()
    start_date = datetime.strptime(start_from, "%Y-%m-%d").date()

    # Convert streak dates to date objects
    streak_dates_dt = set([datetime.strptime(d, "%Y-%m-%d").date() for d in streak_dates])

    # All dates from start_date to yesterday
    all_days = [start_date + timedelta(days=i) for i in range((today - start_date).days)]

    # Failed dates = all days not in streaks
    failed_dates = [d.strftime("%Y-%m-%d") for d in all_days if d not in streak_dates_dt]

    #print(f"[DEBUG] Streak dates: {sorted(streak_dates_dt)}")
    #print(f"[DEBUG] Failed dates: {failed_dates}")

    return failed_dates

def calculate_rewards(db: Session, user_id: int):
    """
    Diamonds: +1 for each correctly spelled word, -2 for each wrong word.
    Rubies: will be implemented similarly for vocabulary later.
    """
    total_correct = db.query(func.count()).filter(
        UserActivity.user_id == user_id, UserActivity.is_correct == True
    ).scalar() or 0

    total_wrong = db.query(func.count()).filter(
        UserActivity.user_id == user_id, UserActivity.is_correct == False
    ).scalar() or 0
    print('/n')
    print("total_correct:", total_correct, "total_wrong:", total_wrong)
    # Diamond logic
    #diamonds = total_correct - (2 * total_wrong)
    diamonds = total_correct - ( total_wrong)
    diamonds = max(diamonds, 0)  # Ensure not negative

    # Placeholder for rubies (vocabulary)
    rubies = 0

    return diamonds, rubies


def get_dashboard_data(db: Session, user_id: int):
    """Return all dashboard data needed for frontend, safely handling None values."""

    # --- Fetch user activity ---
    activities = db.query(UserActivity).filter(UserActivity.user_id == user_id).all()

    # --- Streak Dates ---
    streak_dates = [a.timestamp.strftime("%Y-%m-%d") for a in activities if a.timestamp]
    failed_dates = calculate_failed_dates(streak_dates, start_from="2025-08-01")

    # --- Totals ---
    total_correct = (
        db.query(func.count())
        .filter(UserActivity.user_id == user_id, UserActivity.is_correct == True)
        .scalar() or 0
    )

    total_wrong = (
        db.query(func.count())
        .filter(UserActivity.user_id == user_id, UserActivity.is_correct == False)
        .scalar() or 0
    )

    total_words = db.query(Word).count() or 0

    # --- Accuracy ---
    accuracy = (
        round(total_correct / (total_correct + total_wrong) * 100, 2)
        if (total_correct + total_wrong) > 0
        else 0
    )

    # --- Mastered Words ---
    mastered_words = (
        db.query(func.count(func.distinct(UserActivity.word_id)))
        .filter(UserActivity.user_id == user_id, UserActivity.is_correct == True)
        .group_by(UserActivity.word_id)
        .having(func.count(UserActivity.word_id) >= 10)
        .all()
    )
    mastered_count = len(mastered_words)

    # --- Never Spelled Words ---
    attempted_words = (
        db.query(func.count(func.distinct(UserActivity.word_id)))
        .filter(UserActivity.user_id == user_id)
        .scalar() or 0
    )
    never_spelled = total_words - attempted_words

    # --- Last 10 Days Progress ---
    recent_data = (
        db.query(
            func.date(UserActivity.timestamp).label("day"),
            func.sum(case((UserActivity.is_correct == True, 1), else_=0)).label("correct"),
            func.sum(case((UserActivity.is_correct == False, 1), else_=0)).label("wrong"),
        )
        .filter(UserActivity.user_id == user_id)
        .group_by(func.date(UserActivity.timestamp))
        .order_by(func.date(UserActivity.timestamp).desc())
        .limit(10)
        .all()
    )

    # Format recent data safely
    days = [r.day.strftime("%Y-%m-%d") for r in recent_data if r.day is not None][::-1]
    correct_counts = [int(r.correct or 0) for r in recent_data if r.day is not None][::-1]
    wrong_counts = [int(r.wrong or 0) for r in recent_data if r.day is not None][::-1]
    accuracy_by_day = [
        round((r.correct / (r.correct + r.wrong) * 100), 2)
        if (r.correct + r.wrong) > 0 else 0
        for r in recent_data if r.day is not None
    ][::-1]

    # Distinct grade levels for dropdown
    grade_levels = [g[0] for g in db.query(distinct(Word.grade_level)).order_by(Word.grade_level).all()]

    # --- Rewards ---
    diamonds, rubies = calculate_rewards(db, user_id)

    # --- Return all data ---
    return {
        "streak_dates": streak_dates,
        "failed_dates": failed_dates,
        "accuracy": accuracy,
        "total_correct": total_correct,
        "total_wrong": total_wrong,
        "total_words": total_words,
        "never_spelled": never_spelled,
        "mastered": mastered_count,
        "days": days,
        "correct_counts": correct_counts,
        "wrong_counts": wrong_counts,
        "accuracy_by_day": accuracy_by_day,
        "grade_levels": grade_levels,
        "diamonds": diamonds,
        "rubies": rubies
    }
