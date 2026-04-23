from flask import Flask, render_template, abort
import json
import os

app = Flask(__name__)


def load_stats():
    """Safely load the stats.json file."""
    try:
        # Assumes stats.json is in the root directory next to app.py
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

    # Dynamically generate the roster list based on the keys in stats.json
    roster = list(members_data.keys())

    # Pass the roster and the full data dictionary to index.html
    return render_template('index.html', roster=roster, members=members_data)


@app.route('/member/<username>')
def member_profile(username):
    """Render the individual member profile page."""
    members_data = load_stats()

    # Ensure the requested member exists in the database
    if username not in members_data:
        abort(404)  # Return a 404 Not Found error if they don't exist

    member_info = members_data[username]

    # Pass the specific member's data to member.html
    return render_template(
        'member.html',
        name=username,
        username=username,
        info=member_info
    )


if __name__ == "__main__":
    # Render assigns a dynamic port. This ensures the app binds to it correctly.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)