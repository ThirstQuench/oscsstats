from flask import Flask, render_template, abort
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# The OSCS Roster
MEMBERS = [
    'sunnys', 'santipulgaz', 'youngbasedgo', 'arky',
    'yugi2x', 'nosiiree', '1jdab1', 'redify', 'bigmonraph'
]

DATA_FILE = 'data/stats.json'


def get_cached_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}


@app.route('/')
def index():
    all_stats = get_cached_data()
    # Logic to show 'Data Loading' if stats.json is empty
    return render_template('index.html', members=all_stats, roster=MEMBERS)


@app.route('/member/<username>')
def member_detail(username):
    all_stats = get_cached_data()
    # Normalize name to match dictionary keys
    user_key = username.lower()

    if user_key not in all_stats:
        # If they are in the roster but data isn't fetched yet
        if user_key in MEMBERS:
            return render_template('member.html', name=username, info=None)
        abort(404)

    return render_template('member.html', name=username, info=all_stats[user_key])


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(debug=True)