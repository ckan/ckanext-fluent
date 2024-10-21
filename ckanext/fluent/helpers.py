from ckan.lib.i18n import get_available_locales

from ckanext.scheming.helpers import scheming_language_text


def fluent_form_languages(field=None, entity_type=None, object_type=None,
                          schema=None):
    """
    Return a list of language codes for this form (or form field)

    1. return field['form_languages'] if it is defined
    2. return schema['form_languages'] if it is defined
    3. get schema from entity_type + object_type then
       return schema['form_languages'] if they are defined
    4. return languages from site configuration
    """
    if field and 'form_languages' in field:
        return field['form_languages']
    if schema and 'form_languages' in schema:
        return schema['form_languages']
    if entity_type and object_type:
        # late import for compatibility with older ckanext-scheming
        from ckanext.scheming.helpers import scheming_get_schema
        schema = scheming_get_schema(entity_type, object_type)
        if schema and 'form_languages' in schema:
            return schema['form_languages']

    langs = []
    for l in get_available_locales():
        if l.language not in langs:
            langs.append(l.language)
    return langs


def fluent_alternate_languages(field=None, schema=None):
    """
    Return a dict of alternates acceptable as replacements for
    required languages, as given in the field or schema.

    e.g. {'en': ['en-GB']}
    """
    if field and 'alternate_languages' in field:
        return field['alternate_languages']
    if schema and 'alternate_languages' in schema:
        return schema['alternate_languages']
    return {}


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
