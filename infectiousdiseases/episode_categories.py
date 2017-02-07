from opal.core import episodes


class TropicalLiaison(episodes.EpisodeCategory):
    display_name = "Tropical Liaison"
    detail_template = "detail/tropical_liaison.html"

    # don't judge me fix opal#948
    slug = "tropical liaison"
