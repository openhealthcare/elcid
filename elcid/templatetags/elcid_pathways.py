from opal.core.pathway.templatetags.pathways import add_common_context
from django import template

register = template.Library()


@register.inclusion_tag('_helpers/open_multisave.html', takes_context=True)
def open_multisave(
    context, subrecord, add_button_text=None, remove_button_text=None
):
    """
        A multi save that does not collapse anything an always has a minimum
        of one entry (it won't save it if its empty)
    """
    if not add_button_text:
        add_button_text = "Add Another {}".format(subrecord.get_display_name())

    if not remove_button_text:
        remove_button_text = "Remove"

    ctx = add_common_context(context, subrecord)
    ctx["remove_button_text"] = remove_button_text
    ctx["add_button_text"] = add_button_text
    return ctx
