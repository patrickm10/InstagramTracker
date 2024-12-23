import instaloader
import pandas as pd
import os
import time
from dotenv import load_dotenv

# Initialize Instaloader
L = instaloader.Instaloader()

# Load environment variables
load_dotenv()

# Login to Instagram
username = os.getenv('USRNAME')
pwd = os.getenv('PWD')

if not username or not pwd:
    print("Username or password not found in environment variables.")
    exit()

try:
    # Use a session file if available
    try:
        L.load_session_from_file(username)
    except FileNotFoundError:
        print("Session file not found, logging in...")
        L.login(username, pwd)
        L.save_session_to_file()

    print(f"Logged in as {username}")

    # Get profile
    profile = instaloader.Profile.from_username(L.context, username)

    # Fetch followers and following
    time.sleep(10)  # Delay to prevent rate limiting
    followers = set(profile.get_followers())

    time.sleep(10)  # Delay to prevent rate limiting
    following = set(profile.get_followees())

    # Convert to DataFrames
    followers_df = pd.DataFrame([f.username for f in followers], columns=['username'])
    following_df = pd.DataFrame([f.username for f in following], columns=['username'])

    # Find followers that you are not following back
    not_following_back = followers_df[~followers_df['username'].isin(following_df['username'])]

    # Find following that are not following you back
    not_followed_back = following_df[~following_df['username'].isin(followers_df['username'])]

    # Print results
    print("Followers that you are not following back:", not_following_back['username'].tolist())
    print("Following that are not following you back:", not_followed_back['username'].tolist())

except instaloader.exceptions.ConnectionException as e:
    print(f"Connection error: {e}")
    print("Please wait and try again later.")
