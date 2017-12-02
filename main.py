import argparse
import sys

import reddit
import sidebar

FAILURE_MESSAGE = """
I couldn't parse the sidebar text correctly. Somewhere in the sidebar, 
there should be a link in the form `[Text to be replaced](
.../r/SUB_NAME/submit...)` where the `...` is anything and `SUB_NAME` is the 
name of your subreddit. 

Subreddit closing or opening will have to be done manually."""


def main():
    args = get_options()
    if args.open == args.close:
        print('Exactly one of -o or -c must be provided.')
        sys.exit(1)
    if not reddit.has_permissions():
        print('Insufficient permissions.')
        sys.exit(1)
    old_sb_text = reddit.get_sidebar()

    try:
        new_sb_text = sidebar.update_sidebar_text(old_sb_text,
                                                  args.button_text,
                                                  reddit.get_sub_name())
    except sidebar.SidebarError:
        print('Failed parsing sidebar. Sending failure message.')
        reddit.message_mods(FAILURE_MESSAGE)
        sys.exit(1)

    make_open = args.open if args.open else False
    reddit.update_settings(new_sb_text, make_open)

    print('Success.')


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--open', action='store_true',
                        help='open the subreddit')
    parser.add_argument('-c', '--close', action='store_true',
                        help='close the subreddit')
    parser.add_argument('button_text', help='text to go on the submit button.')
    return parser.parse_args()


if __name__ == '__main__':
    main()
