import sidebar


def test_sidebar():
    no_link_sidebar = 'Hello World.'
    no_br_sidebar = 'Click here(https://www.reddit.com/r/PokemonCreate/' \
                    'submit?selftext=true&title=[PokeRequest][Gen7]'
    no_cbr_sidebar = '[Click here(https://www.reddit.com/r/PokemonCreate/' \
                     'submit?selftext=true&title=[PokeRequest][Gen7]'
    no_obr_sidebar = 'Click here](https://www.reddit.com/r/PokemonCreate/' \
                     'submit?selftext=true&title=[PokeRequest][Gen7]'
    wrong_order_br = ']Click here[(https://www.reddit.com/r/PokemonCreate/' \
                     'submit?selftext=true&title=[PokeRequest][Gen7]'
    proper_sidebar = '[Click here](https://www.reddit.com/r/PokemonCreate/' \
                     'submit?selftext=true&title=[PokeRequest][Gen7]'
    newline_sidebar = '[Click here]\n(https://www.reddit.com/r/PokemonCreate/' \
                      'submit?selftext=true&title=[PokeRequest][Gen7]'

    replacement_text = 'Closed'

    def throws_error(txt):
        try:
            sidebar.update_sidebar_text(txt, replacement_text, 'PokemonCreate')
        except sidebar.SidebarError:
            assert True
        else:
            assert False

    throws_error(no_link_sidebar)
    throws_error(no_br_sidebar)
    throws_error(no_cbr_sidebar)
    throws_error(no_obr_sidebar)
    throws_error(wrong_order_br)

    try:
        got = sidebar.update_sidebar_text(proper_sidebar, replacement_text,
                                          'PokemonCreate')
    except sidebar.SidebarError:
        assert False
    else:
        assert got == '[Closed](https://www.reddit.com/r/PokemonCreate/' \
                      'submit?selftext=true&title=[PokeRequest][Gen7]'

    try:
        got = sidebar.update_sidebar_text(newline_sidebar, replacement_text,
                                          'PokemonCreate')
    except sidebar.SidebarError:
        assert False
    else:
        assert got == '[Closed]\n(https://www.reddit.com/r/PokemonCreate/' \
                      'submit?selftext=true&title=[PokeRequest][Gen7]'
