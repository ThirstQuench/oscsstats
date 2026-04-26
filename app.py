from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)

# ==========================================
# X / TWITTER OVERRIDES
# ==========================================
# By default, the app assumes their Twitter is the exact same as their master key.
# We map the lowercase master key to their actual X/Twitter handle here.

TWITTER_OVERRIDES = {
    "sunnys": "sunnysirl",
    "youngbasedgo": "YOUNGBASEDG",
    "arky": "ArkySZNN",
    "redify": "redifyys"
}


def load_stats():
    try:
        with open('stats.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Warning: stats.json not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: stats.json is corrupted.")
        return {}


@app.route('/')
def index():
    members_data = load_stats()
    roster = list(members_data.keys())
    return render_template('index.html', roster=roster, members=members_data)


@app.route('/member/<username>')
def member_profile(username):
    members_data = load_stats()

    if username not in members_data:
        abort(404)

    member_info = members_data[username]

    # Check if they have a different Twitter name. If not, just use their Twitch name.
    twitter_handle = TWITTER_OVERRIDES.get(username.lower(), username)

    return render_template(
        'member.html',
        name=username,  # The master Twitch name
        twitter_handle=twitter_handle,  # The specific X/Twitter link
        info=member_info
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)