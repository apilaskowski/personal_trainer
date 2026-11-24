"""
Hevy REST API Client for Personal Trainer.
Handles fetching workouts, on-demand template synchronization,
and muscle group normalization directly from Hevy's official database.
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

HEVY_API_BASE = "https://api.hevyapp.com/v1"
_CACHE_FILE = os.path.join(os.path.dirname(__file__), "hevy_templates_cache.json")

# Normalizes Hevy's official API muscle group strings into our 10 standard groups
HEVY_MUSCLE_NORMALIZATION = {
    "quadriceps": "Quads",
    "quads": "Quads",
    "hamstrings": "Hamstrings",
    "glutes": "Glutes",
    "calves": "Calves",
    "chest": "Chest",
    "lats": "Back",
    "upper_back": "Back",
    "lower_back": "Back",
    "traps": "Back",
    "trapezius": "Back",
    "shoulders": "Shoulders",
    "deltoids": "Shoulders",
    "biceps": "Biceps",
    "triceps": "Triceps",
    "forearms": "Biceps",
    "abdominals": "Abs",
    "abs": "Abs",
    "core": "Abs",
    "obliques": "Abs"
}

def normalize_hevy_muscle(muscle_name: str) -> str:
    """Normalizes a raw muscle string from Hevy to a standard group name."""
    if not muscle_name:
        return None
    key = muscle_name.lower().replace(" ", "_").strip()
    return HEVY_MUSCLE_NORMALIZATION.get(key)

def load_templates_cache() -> dict:
    """Loads the cached exercise templates from disk."""
    if os.path.exists(_CACHE_FILE):
        try:
            with open(_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {k: v for k, v in data.items() if not k.startswith("_")}
        except Exception as e:
            print(f"[Warning] Could not load templates cache: {e}")
    return {}

def save_templates_cache(cache: dict):
    """Persists updated templates cache to disk."""
    try:
        data = {"_comment": "Cached Hevy exercise templates. Auto-updated on-demand."}
        data.update(cache)
        with open(_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[Warning] Could not save templates cache: {e}")

# In-memory template cache
_CACHED_TEMPLATES = load_templates_cache()

def fetch_template_from_hevy(template_id: str, api_key: str) -> list[str]:
    """Fetches a single exercise template from Hevy API by its ID."""
    if not template_id or not api_key:
        return []

    url = f"{HEVY_API_BASE}/exercise_templates/{template_id}"
    headers = {
        "api-key": api_key,
        "Accept": "application/json",
        "User-Agent": "PersonalTrainer-App"
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            template = data.get("exercise_template", data)

            muscles = []
            primary = normalize_hevy_muscle(template.get("primary_muscle_group"))
            if primary:
                muscles.append(primary)

            for sec in template.get("secondary_muscle_groups", []):
                norm = normalize_hevy_muscle(sec)
                if norm and norm not in muscles:
                    muscles.append(norm)

            title = template.get("title", "")
            print(f"[Hevy API] Synced template: '{title}' ({template_id}) -> {muscles}")
            return muscles
    except urllib.error.HTTPError as e:
        print(f"[Warning] Could not fetch Hevy template {template_id} (HTTP {e.code})")
    except Exception as e:
        print(f"[Warning] Error fetching template {template_id}: {e}")

    return []

def resolve_exercise_muscles(exercise_title: str, template_id: str = None, api_key: str = None) -> list[str]:
    """
    Resolves an exercise to its target muscle groups directly from Hevy:
    1. Checks if template_id is in local cache (0 API calls).
    2. If missing from cache and api_key is available, queries Hevy API and updates cache.
    3. If neither is available, matches against titles in cache.
    """
    global _CACHED_TEMPLATES

    # 1. Check local cache by template_id
    if template_id and template_id in _CACHED_TEMPLATES:
        cached_muscles = _CACHED_TEMPLATES[template_id].get("muscles")
        if cached_muscles:
            return cached_muscles

    # 2. On-demand pull from Hevy API for new/unknown exercises
    if template_id and api_key:
        fetched_muscles = fetch_template_from_hevy(template_id, api_key)
        if fetched_muscles:
            _CACHED_TEMPLATES[template_id] = {
                "title": exercise_title,
                "muscles": fetched_muscles
            }
            save_templates_cache(_CACHED_TEMPLATES)
            return fetched_muscles

    # 3. Match against cached titles as a fallback
    title_lower = (exercise_title or "").lower().strip()
    for cached_id, t_info in _CACHED_TEMPLATES.items():
        if t_info.get("title", "").lower().strip() == title_lower:
            return t_info.get("muscles", [])

    return []

def get_workouts(api_key: str = None, page_count: int = 5) -> list[dict]:
    """
    Fetches recent workouts from the Hevy API.
    Strictly requires HEVY_API_KEY.
    """
    api_key = api_key or os.environ.get("HEVY_API_KEY")

    if not api_key:
        raise ValueError("HEVY_API_KEY is required to fetch workouts from Hevy API.")

    headers = {
        "api-key": api_key,
        "Accept": "application/json",
        "User-Agent": "PersonalTrainer-App"
    }

    all_workouts = []
    page = 1
    page_size = 10

    while page <= page_count:
        url = f"{HEVY_API_BASE}/workouts?page={page}&pageSize={page_size}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                workouts = data.get("workouts", [])
                if not workouts:
                    break
                all_workouts.extend(workouts)
                page += 1
        except urllib.error.HTTPError as e:
            print(f"[Error] Failed to fetch Hevy workouts (HTTP {e.code}): {e.read().decode('utf-8')}")
            break
        except Exception as e:
            print(f"[Error] Failed to connect to Hevy API: {e}")
            break

    print(f"Successfully fetched {len(all_workouts)} workouts from Hevy API.")
    return all_workouts
