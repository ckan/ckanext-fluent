from ckan.lib.i18n import get_available_locales

from ckan.plugins.toolkit import (
    h, chained_helper, get_action, ObjectNotFound, NotAuthorized
)


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
        schema = h.scheming_get_schema(entity_type, object_type)
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
    the standard label or field name.
    """
    form_label = field.get('fluent_form_label', {})

    if lang in form_label:
        return h.scheming_language_text(form_label[lang])

    return lang.upper() + ' ' + h.scheming_language_text(
        field.get('label', field['field_name'])
    )


@chained_helper
def scheming_missing_required_fields(
        next_helper, pages, data=None, package_id=None):
    """
    """
    if package_id:
        try:
            data = get_action('package_show')({}, {"id": package_id})
        except (ObjectNotFound, NotAuthorized):
            pass
    if data is None:
        data = {}
    missing = next_helper(pages, data, package_id)
    if not data.get('type'):
        return missing

    schema = h.scheming_get_dataset_schema(data['type'])
    for page_missing, page in zip(missing, pages):
        for f in page['fields']:
            if (
                f['field_name'] not in data
                or f['field_name'] in page_missing
                or 'validators' not in f
                or not any(v.startswith('fluent_') for v in f['validators'].split())
                or not f.get('required')
            ):
                continue
            required_langs = fluent_form_languages(f, schema=schema)
            alternate_langs = fluent_alternate_languages(f, schema=schema)
            value = data[f['field_name']]
            for lang in required_langs:
                if value.get(lang) or any(
                    value.get(l) for l in alternate_langs.get(lang, [])
                ):
                    continue
                page_missing.append(f['field_name'])
                break
    return missing
