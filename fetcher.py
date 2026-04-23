import os
import requests
import json
import time

MEMBERS = ['sunnys', 'santipulgaz', 'youngbasedgo', 'arky', 'yugi2x', 'nosiiree', '1jdab1', 'redify', 'bigmonraph']


def fetch_all():
    if not os.path.exists('data'):
        os.makedirs('data')


    results = {}
    print("Starting OSCS Data Fetch...")

    for member in MEMBERS:
        print(f"Fetching {member}...")
        try:
            # 1. Channel Summary
            r = requests.get(f"https://twitchtracker.com/api/channels/summary/{member}")
            if r.status_code == 200:
                results[member] = r.json()
                # 2. Category Summary (Optional: Pulling more specific game data)
                # For now, we stick to the primary summary to avoid rate limits
            else:
                print(f"Failed to get {member}: {r.status_code}")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(2)  # Be nice to the API

    with open('stats.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Done!")


if __name__ == "__main__":
    fetch_all()