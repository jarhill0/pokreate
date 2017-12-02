import sys

import praw
import prawcore

USER_AGENT = 'Pokreate v0.1'

try:
    import config
except ImportError:
    print('Could not load settings. Rename EXAMPLE_config.py to config.py and'
          'fill out its information.')
    sys.exit(1)

if not all((config.password, config.client_id, config.client_secret)):
    try:
        reddit = praw.Reddit(config.username, user_agent=USER_AGENT)
    except Exception:
        print('Could not log in with site_name "{}"'.format(config.username))
        sys.exit(1)
else:
    try:
        reddit = praw.Reddit(username=config.username,
                             password=config.password,
                             client_id=config.client_id,
                             client_secret=config.client_secret,
                             user_agent=USER_AGENT)
    except Exception:
        print('Could not log in.')
        sys.exit(1)

try:
    reddit.user.me()
except prawcore.exceptions.PrawcoreException:
    print('Bad login information.')
    sys.exit(1)


def get_sidebar():
    return reddit.subreddit(config.subreddit).mod.settings()['description']


def get_sub_name():
    return config.subreddit


def has_permissions():
    my_permissions = []

    try:
        for m in reddit.subreddit(config.subreddit).moderator(reddit.user.me()):
            my_permissions = m.mod_permissions
    except (praw.exceptions.PRAWException, prawcore.PrawcoreException):
        print("Permission check failed.")
        return False

    return 'all' in my_permissions or 'config' in my_permissions


def message_mods(msg):
    reddit.subreddit(config.subreddit).message(subject='Bot message',
                                               message=msg)


def update_settings(sidebar, is_public):
    sub_type = 'public' if is_public else 'restricted'
    reddit.subreddit(config.subreddit).mod.update(subreddit_type=sub_type,
                                                  description=sidebar)
