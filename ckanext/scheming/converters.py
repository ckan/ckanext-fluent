import json

from ckan.plugins.toolkit import missing

def scheming_multilingual_text(key, data, errors, context):
    """
    Accept multilingual text input in the following forms
    and convert to a json string for storage:

    1. a multilingual dict, eg.

       {"en": "Text", "fr": "texte"}

    2. a JSON encoded version of a multilingual dict, for
       compatibility with old ways of loading data, eg.

       '{"en": "Text", "fr": "texte"}'

    3. separate fields per language (for form submissions):

       fieldname-en = "Text"
       fieldname-fr = "texte"
    """
    value = data[key]
    if value is not missing:
        if isinstance(value, dict):
            data[key] = json.dumps(value) # 1. multilingual dict
        # FIXME: assuming it's an already-encoded dict
        return

    # 3. separate fields
    output = {}
    prefix = key[0] + '-'
    extras = data.get(('__extras',), {})

    for name, text in extras.iteritems():
        if name.startswith(prefix):
            output[name.split('-', 1)[1]] = text
    for lang in output:
        del extras[prefix + lang]
    data[key] = json.dumps(output)


def scheming_multilingual_text_output(value):
    """
    Return stored json representation as a multilingual dict, if
    value is already a dict just pass it through.
    """
    if isinstance(value, dict):
        return value
    return json.loads(value)
