from ckan.lib.helpers import get_available_locales

from ckanext.scheming.helpers import scheming_language_text


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

def fluent_form_label(field, lang):
    """
    Return a label for the input field for the given language

    If the field has a fluent_form_label defined the label will
    be taken from there.  If a matching label can't be found
    this helper will return the language code in uppercase and
    the standard label.
    """
    form_label = field.get('fluent_form_label', {})

    if lang in form_label:
        return scheming_language_text(form_label[lang])

    return lang.upper() + ' ' + scheming_language_text(field['label'])
