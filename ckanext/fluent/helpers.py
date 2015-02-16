
from ckan.lib.helpers import get_available_locales

def fluent_form_languages(schema, field=None):
    """
    Return a list of language codes for this form (or form field)

    1. return field['form_languages'] if it is defined
    2. return schema['form_languages'] if it is defined
    3. return languages from site configuration
    """
    if 'form_languages' in field:
        return field['form_languages']
    if 'form_languages' in schema:
        return schema['form_languages']

    langs = []
    for l in get_available_locales():
        if l.language not in langs:
            langs.append(l.language)
    return langs
