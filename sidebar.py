def update_sidebar_text(old_text, new_link_text, sub_name):
    try:
        link_index = old_text.lower().index('/r/{}/submit'.format(
            sub_name.lower()))
    except ValueError:
        raise SidebarError('Could not find submit link.')

    # find the link text brackets
    # note: unexpected behavior if the link or its text contains "[" or "]"
    section = old_text[:link_index]

    if ']' not in section:
        raise SidebarError('Could not find closing bracket.')
    cbr = section.rfind(']')

    section = section[:cbr]
    if '[' not in section:
        raise SidebarError('Could not find opening bracket.')
    obr = section.rfind('[')

    return old_text[:obr + 1] + new_link_text + old_text[cbr:]


class SidebarError(ValueError):
    """Raised when the sidebar can't be parsed properly."""
    pass
