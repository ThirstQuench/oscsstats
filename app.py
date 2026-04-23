from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)

# ==========================================
# OSCS ROSTER MASTER DIRECTORY
# ==========================================

# Exact X / Twitter Handles
TWITTER_HANDLES = {
    "sunny": "sunnysirl",
    "santi": "santipulgaz",
    "ybg": "YOUNGBASEDG",
    "arky": "ArkySZNN",
    "yugi": "yugi2x",
    "nosiiree": "Nosiiree",
    "jdab": "1JDAB1",
    "redify": "redifyys",
    "bigmonraph": "BigMonRaph"
}

# Exact Twitch Usernames (Useful if stats.json keys have weird capitalization)
TWITCH_USERNAMES = {
    "sunny": "sunnysirl",
    "santi": "santipulgaz",
    "ybg": "YOUNGBASEDG",
    "arky": "ArkySZNN",
    "yugi": "yugi2x",
    "nosiiree": "Nosiiree",
    "jdab": "1JDAB1",
    "redify": "redifyys",
    "bigmonraph": "BigMonRaph"
}

# Future Expansion: YouTube Channel IDs or Handles
YOUTUBE_CHANNELS = {
    # "member_key": "youtube_handle_here"
}


# ==========================================
# DATABASE & ROUTING LOGIC
# ==========================================

def load_stats():
    """Safely load the stats.json file."""
    try:
        with open('stats.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Warning: stats.json not found. Returning empty dataset.")
        return {}
    except json.JSONDecodeError:
        print("Error: stats.json is corrupted or not valid JSON.")
        return {}


@app.route('/')
def index():
    """Render the homepage dashboard."""
    members_data = load_stats()
    roster = list(members_data.keys())

    # Passing both the raw data and the custom Twitch names to the frontend
    return render_template(
        'index.html',
        roster=roster,
        members=members_data,
        twitch_map=TWITCH_USERNAMES
    )


@app.route('/member/<username>')
def member_profile(username):
    """Render the individual member profile page."""
    members_data = load_stats()

    if username not in members_data:
        abort(404)

    member_info = members_data[username]

    # Force lowercase for dictionary lookups to prevent case-sensitivity crashes
    lookup_key = username.lower()

    # Pull the exact handles from our Master Directory, default to username if missing
    actual_twitter = TWITTER_HANDLES.get(lookup_key, username)
    actual_twitch = TWITCH_USERNAMES.get(lookup_key, username)
    actual_youtube = YOUTUBE_CHANNELS.get(lookup_key, "")

    return render_template(
        'member.html',
        name=username,
        info=member_info,
        twitch_handle=actual_twitch,
        twitter_handle=actual_twitter,
        youtube_handle=actual_youtube
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)