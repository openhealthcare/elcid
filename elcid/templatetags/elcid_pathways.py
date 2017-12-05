from opal.core.pathway.templatetags.pathways import add_common_context
from django import template

register = template.Library()


@register.inclusion_tag('_helpers/open_multisave.html', takes_context=True)
def open_multisave(context, subrecord):
    """
        A multi save that does not collapse anything an always has a minimum
        of one entry (it won't save it if its empty)
    """
    return add_common_context(context, subrecord)
