import json

from ckan.plugins.toolkit import get_validator, _

from ckanext.fluent.helpers import fluent_form_languages

try:
    from ckanext.scheming.validation import scheming_validator
except ImportError:
    # If scheming can't be imported, replace our validators that require it
    # with a noop
    def scheming_validator(fn):
        def noop(value):
            return value
        return noop

ignore_missing = get_validator('ignore_missing')

@scheming_validator
def fluent_scheming_required(field, schema):
    """
    When field is marked required require all languages that
    appear in the form to be given.

    This validator is meant to be called after fluent_text
    so that all fields are represented as a single dict
    """
    if not field.get('required'):
        return ignore_missing
    langs = fluent_form_languages(schema, field)
    def validator(key, data, errors, context):
        value = json.loads(data[key])
        for l in langs:
            v = value.get(l)
            if not v:
                errors[key].append(_('Required language "%s" missing') % l)
    return validator
