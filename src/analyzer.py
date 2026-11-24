"""
Workout Analysis and Recommendation Engine for Personal Trainer.
Computes:
- 48-Hour Independent Muscle Recovery States.
- Rolling 7-day and 14-day working set volumes vs. weekly targets.
- Prioritized 'What to Train Today' focus recommendations.
"""

from datetime import datetime, timezone
from src.config import (
    DEFAULT_WEEKLY_GOALS,
    DEFAULT_RECOVERY_THRESHOLDS,
    DEFAULT_RECOVERY_HOURS
)
from src.hevy_client import resolve_exercise_muscles

def parse_iso(dt_str: str) -> datetime:
    """Parses an ISO format date string into a timezone-aware UTC datetime."""
    if not dt_str:
        return datetime.now(timezone.utc)
    # Python 3.11+ standard library natively supports 'Z' and offset formats
    return datetime.fromisoformat(dt_str)

def analyze_workouts(
    workouts: list[dict],
    weekly_goals: dict = None,
    recovery_thresholds: dict = None,
    current_time: datetime = None,
    api_key: str = None
) -> dict:
    """
    Analyzes workout logs to determine recovery states, volume deficits, and recommendations.
    Accepts an optional current_time for deterministic testing, and api_key for on-demand template resolution.
    """
    weekly_goals = weekly_goals or DEFAULT_WEEKLY_GOALS
    recovery_thresholds = recovery_thresholds or DEFAULT_RECOVERY_THRESHOLDS
    now = current_time or datetime.now(timezone.utc)

    # Initialize stats per muscle group
    muscle_stats = {}
    for muscle, target in weekly_goals.items():
        threshold = recovery_thresholds.get(muscle, DEFAULT_RECOVERY_HOURS)
        muscle_stats[muscle] = {
            "name": muscle,
            "weekly_target": target,
            "recovery_threshold_hours": threshold,
            "sets_7d": 0,
            "sets_14d": 0,
            "last_trained": None,
            "hours_since_last": None,
            "recovery_status": "ready",
            "recovery_percent": 100
        }

    # Process all workouts chronologically descending
    processed_workouts = []
    sorted_workouts = sorted(workouts, key=lambda x: parse_iso(x.get("start_time")), reverse=True)

    for w in sorted_workouts:
        w_time = parse_iso(w.get("start_time"))
        hours_ago = max(0.0, (now - w_time).total_seconds() / 3600.0)
        days_ago = hours_ago / 24.0

        workout_muscles_hit = set()
        total_working_sets = 0

        for ex in w.get("exercises", []):
            title = ex.get("title", "")
            template_id = ex.get("exercise_template_id")
            # Resolves via on-demand Hevy cache
            muscle_weights = resolve_exercise_muscles(title, template_id=template_id, api_key=api_key)

            # Count working sets (exclude warmups)
            working_sets = sum(
                1 for s in ex.get("sets", [])
                if s.get("set_type") in ("normal", "failure", "drop_set", None)
            )
            total_working_sets += working_sets

            for m, weight in muscle_weights.items():
                if m in muscle_stats:
                    workout_muscles_hit.add(m)
                    # Update most recent workout timestamp
                    if muscle_stats[m]["last_trained"] is None or w_time > muscle_stats[m]["last_trained"]:
                        muscle_stats[m]["last_trained"] = w_time
                        muscle_stats[m]["hours_since_last"] = round(hours_ago, 1)

                    # Rolling volume windows (1.0 primary, 0.5 secondary)
                    earned = working_sets * weight
                    if days_ago <= 7.0:
                        muscle_stats[m]["sets_7d"] += earned
                    if days_ago <= 14.0:
                        muscle_stats[m]["sets_14d"] += earned

        processed_workouts.append({
            "id": w.get("id"),
            "title": w.get("title") or "Workout Session",
            "date": w_time.strftime("%Y-%m-%d %H:%M"),
            "hours_ago": round(hours_ago, 1),
            "total_sets": total_working_sets,
            "muscles": sorted(list(workout_muscles_hit))
        })

    # Compute recovery states, volume deficits, and formatting
    for m, stat in muscle_stats.items():
        hrs = stat["hours_since_last"]
        threshold = stat.get("recovery_threshold_hours", DEFAULT_RECOVERY_HOURS)
        half_recovery = threshold / 2.0

        if hrs is None:
            # Never trained in window -> fully rested and ready
            stat["recovery_status"] = "ready"
            stat["recovery_percent"] = 100
            stat["hours_since_last"] = 999.0
            stat["rest_label"] = "Rested (> 7 days)"
        elif hrs >= threshold:
            stat["recovery_status"] = "ready"
            stat["recovery_percent"] = 100
            days = round(hrs / 24.0, 1)
            stat["rest_label"] = f"{days}d ago ({int(hrs)}h)"
        elif hrs >= half_recovery:
            stat["recovery_status"] = "recovering"
            stat["recovery_percent"] = round((hrs / threshold) * 100)
            stat["rest_label"] = f"{int(hrs)}h ago (Recovering)"
        else:
            stat["recovery_status"] = "resting"
            stat["recovery_percent"] = round((hrs / threshold) * 100)
            stat["rest_label"] = f"{int(hrs)}h ago (Resting)"

        # Convert datetime to ISO string for clean JSON serialization
        if stat["last_trained"]:
            stat["last_trained"] = stat["last_trained"].isoformat()

        # Clean numerical formatting (format whole numbers as ints, half sets as floats)
        def clean_val(v: float):
            r = round(v, 1)
            return int(r) if r % 1 == 0 else r

        stat["sets_7d"] = clean_val(stat["sets_7d"])
        stat["sets_14d"] = clean_val(stat["sets_14d"])

        # Progress and deficit
        stat["progress_7d"] = round((stat["sets_7d"] / stat["weekly_target"]) * 100)
        stat["deficit_7d"] = clean_val(max(0.0, stat["weekly_target"] - stat["sets_7d"]))

    # Determine "What to Train Today"
    # Rule: Filter for READY muscles (met full required recovery window), sort by largest volume deficit
    ready_muscles = [s for s in muscle_stats.values() if s["recovery_status"] == "ready"]
    ready_muscles.sort(key=lambda x: (x["deficit_7d"], -x["sets_7d"]), reverse=True)

    recommended_focus = [m["name"] for m in ready_muscles if m["deficit_7d"] > 0][:4]
    if not recommended_focus:
        # All target goals met, pick the most rested muscles
        recommended_focus = [m["name"] for m in ready_muscles[:3]]

    headline = f"Today's Focus: {', '.join(recommended_focus)}" if recommended_focus else "All Muscles Resting"

    return {
        "generated_at": now.strftime("%Y-%m-%d %H:%M UTC"),
        "today_recommendation": {
            "focus_muscles": recommended_focus,
            "headline": headline,
            "summary": "These muscles have had full required rest and are currently highest priority for your rolling 7-day volume goals."
        },
        "muscles": list(muscle_stats.values()),
        "recent_workouts": processed_workouts[:6]
    }
