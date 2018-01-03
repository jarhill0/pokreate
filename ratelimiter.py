"""Standalone script to remove posts made by a user more than once per day."""

import logging
import os
import sys
import time

import praw
import prawcore

import config

LOG_FILE = os.path.join(os.path.dirname(__file__), 'ratelimiter.log')

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.WARNING)

USER_AGENT = 'pokreate rate limiter'
RUN_FREQUENCY = 30 * 60  # in seconds. Assumes it will always be run this often.
POST_WINDOW = 60 * 60 * 24  # "rate limit" to check posts in, in seconds.
REMOVAL_MESSAGE = 'Removed. You may only submit 1 request every 24 hours.'

if all((config.username,
        config.password,
        config.client_secret,
        config.client_id)):
    reddit = praw.Reddit(username=config.username,
                         password=config.password,
                         client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent=USER_AGENT)
elif config.username:
    reddit = praw.Reddit(config.username, user_agent=USER_AGENT)
else:
    logging.critical('Login credentials not provided. Exiting.')
    sys.exit(1)

try:
    reddit.user.me()
except:
    logging.critical('Reddit not authenticated properly. Exiting.')
    sys.exit(1)
else:
    logging.info('Logged into Reddit as {}'.format(reddit.user.me()))

NOW = time.time()
removed_this_run = []


def main():
    check_permissions()

    subreddit = reddit.subreddit(config.subreddit)
    mods = list(subreddit.moderator())
    logging.debug('Moderators: {}'.format(mods))

    for post in subreddit.new(limit=None):
        if post.created_utc < NOW - RUN_FREQUENCY:  # we checked it last time
            break

        if post.removed:
            continue

        if post.author in mods:
            continue

        if not allowed(post):
            logging.info('Removing {}'.format(post))
            removed_this_run.append(post.id)  # global object…
            reply = post.reply(REMOVAL_MESSAGE)
            reply.mod.distinguish(sticky=True)
            reply.disable_inbox_replies()
            post.mod.remove()


def allowed(post):
    logging.debug('post = {}'.format(post))
    for other_post in post.author.submissions.new(limit=None):
        logging.debug('other_post = {}'.format(repr(other_post)))
        if other_post.created_utc < NOW - POST_WINDOW:  # old enough; ok
            break

        if other_post == post:  # don't trigger on this same post
            continue

        logging.debug('other_post.removed = {}'.format(other_post.removed))
        if other_post.subreddit == post.subreddit \
                and not (other_post.removed or other_post.banned_by) \
                and other_post.id not in removed_this_run:  # reddit can be a
            # bit slow to update when a post was just removed by this bot
            return False

    return True


def check_permissions():
    my_permissions = []

    try:
        for m in reddit.subreddit(config.subreddit).moderator(reddit.user.me()):
            my_permissions = m.mod_permissions
    except (praw.exceptions.PRAWException, prawcore.PrawcoreException):
        logging.critical('Permission check failed.')
        sys.exit(1)

    if not ('all' in my_permissions or 'posts' in my_permissions):
        logging.critical('Insufficient permissions.')
        sys.exit(1)


if __name__ == '__main__':
    main()
