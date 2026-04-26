from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)

# ==========================================
# OSCS ROSTER MASTER DIRECTORY
# ==========================================
# Keys on the left MUST match your fetcher.py and stats.json exactly.

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

YOUTUBE_CHANNELS = {
    # "sunny": "youtube_id_here"
}


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
    return render_template('index.html', roster=roster, members=members_data)


@app.route('/member/<username>')
def member_profile(username):
    """Render the individual member profile page."""
    members_data = load_stats()

    if username not in members_data:
        abort(404)

    member_info = members_data[username]

    # Look up the correct social handles
    lookup_key = username.lower()
    actual_twitter = TWITTER_HANDLES.get(lookup_key, username)
    actual_youtube = YOUTUBE_CHANNELS.get(lookup_key, "")

    return render_template(
        'member.html',
        name=username,
        username=username,
        info=member_info,
        twitter_handle=actual_twitter,
        youtube_handle=actual_youtube
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)