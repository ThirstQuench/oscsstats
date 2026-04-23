from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)

# ==========================================
# OSCS ROSTER MASTER DIRECTORY
# ==========================================
# The keys here match EXACTLY what comes out of your stats.json
# If a member's X/Twitter handle is different than their Twitch, change it here.

TWITTER_HANDLES = {
    "sunnysirl": "sunnysirl",
    "santipulgaz": "santipulgaz",
    "youngbasedg": "YOUNGBASEDG",
    "arkysznn": "ArkySZNN",
    "yugi2x": "yugi2x",
    "nosiiree": "Nosiiree",
    "1jdab1": "1JDAB1",
    "redifyys": "redifyys",
    "bigmonraph": "BigMonRaph"
}

# Empty list ready for when you add YouTube integration
YOUTUBE_CHANNELS = {
    # "sunnysirl": "youtube_id_here"
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

    # We are back to passing exactly what you used the whole time
    return render_template('index.html', roster=roster, members=members_data)


@app.route('/member/<username>')
def member_profile(username):
    """Render the individual member profile page."""
    members_data = load_stats()

    if username not in members_data:
        abort(404)

    member_info = members_data[username]

    # Look up the Twitter/YouTube handles using the exact Twitch username
    lookup_key = username.lower()
    actual_twitter = TWITTER_HANDLES.get(lookup_key, username)
    actual_youtube = YOUTUBE_CHANNELS.get(lookup_key, "")

    return render_template(
        'member.html',
        name=username,  # The exact Twitch name from stats.json
        username=username,  # Kept identical to what you've always used
        info=member_info,
        twitter_handle=actual_twitter,
        youtube_handle=actual_youtube
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)