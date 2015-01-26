import json
import re

from ckan.plugins.toolkit import missing, _

ISO_639_LANGUAGE = u'^[a-z][a-z][a-z]?[a-z]?$'

def fluent_text(key, data, errors, context):
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
    # just in case there was an error before our validator,
    # bail out here because our errors won't be useful
    if errors[key]:
        return

    value = data[key]
    # 1 or 2. dict or JSON encoded string
    if value is not missing:
        if isinstance(value, basestring):
            try:
                value = json.loads(value)
            except ValueError:
                errors[key].append(_('Failed to decode JSON string'))
                return
            except UnicodeDecodeError:
                errors[key].append(_('Invalid encoding for JSON string'))
                return
        if not isinstance(value, dict):
            errors[key].append(_('expecting JSON object'))
            return

        for lang, text in value.iteritems():
            try:
                m = re.match(ISO_639_LANGUAGE, lang)
            except TypeError:
                errors[key].append(_('invalid type for language code: %r')
                    % lang)
                continue
            if not m:
                errors[key].append(_('invalid language code: "%s"') % lang)
                continue
            if not isinstance(text, basestring):
                errors[key].append(_('invalid type for "%s" value') % lang)
                continue
            if isinstance(text, str):
                try:
                    value[lang] = text.decode('utf-8')
                except UnicodeDecodeError:
                    errors[key]. append(_('invalid encoding for "%s" value')
                        % lang)

        if not errors[key]:
            data[key] = json.dumps(value)
        return

    # 3. separate fields
    output = {}
    prefix = key[-1] + '-'
    extras = data.get(key[:-1] + ('__extras',), {})

    for name, text in extras.iteritems():
        if not name.startswith(prefix):
            continue
        lang = name.split('-', 1)[1]
        m = re.match(ISO_639_LANGUAGE, lang)
        if not m:
            errors[name] = [_('invalid language code: "%s"') % lang]
            output = None
            continue

        if output is not None:
            output[lang] = text

    if output is None:
        return

    for lang in output:
        del extras[prefix + lang]
    data[key] = json.dumps(output)


def fluent_text_output(value):
    """
    Return stored json representation as a multilingual dict, if
    value is already a dict just pass it through.
    """
    if isinstance(value, dict):
        return value
    return json.loads(value)


def fluent_tags(key, data, errors, context):
    """
    Accept multilingual lists of tags in the following forms
    and convert to a json string for storage.

    1. a multilingual dict of lists of tag strings, eg.

       {"en": ["big", "large"], "fr": ["grande"]}

    2. separate fields per language with comma-separated values
       (for form submissions)

       fieldname-en = "big,large"
       fieldname-fr = "grande"
    """
    if errors[key]:
        return

    value = data[key]
    # 1. dict of lists of tag strings
    if value is not missing:
        if not isinstance(value, dict):
            errors[key].append(_('expecting JSON object'))
            return

        for lang, keys in value.items():
            try:
                m = re.match(ISO_639_LANGUAGE, lang)
            except TypeError:
                errors[key].append(_('invalid type for language code: %r')
                    % lang)
                continue
            if not m:
                errors[key].append(_('invalid language code: "%s"') % lang)
                continue
            if not isinstance(keys, list):
                errors[key].append(_('invalid type for "%s" value') % lang)
                continue
            out = []
            for i, v in enumerate(keys):
                if not isinstance(v, basestring):
                    errors[key].append(
                        _('invalid type for "{lang}" value item {num}').format(
                            lang=lang, num=i))
                    continue

                if isinstance(v, str):
                    try:
                        out.append(v.decode('utf-8'))
                    except UnicodeDecodeError:
                        errors[key]. append(_(
                            'expected UTF-8 encoding for '
                            '"{lang}" value item {num}').format(
                                lang=lang, num=i))
                else:
                    out.append(v)
            value[lang] = out

        if not errors[key]:
            data[key] = json.dumps(value)
        return

    # 2. separate fields
    output = {}
    prefix = key[-1] + '-'
    extras = data.get(key[:-1] + ('__extras',), {})

    for name, text in extras.iteritems():
        if not name.startswith(prefix):
            continue
        lang = name.split('-', 1)[1]
        m = re.match(ISO_639_LANGUAGE, lang)
        if not m:
            errors[name] = [_('invalid language code: "%s"') % lang]
            output = None
            continue

        if not isinstance(text, basestring):
            errors[name].append(_('invalid type'))
            continue

            if isinstance(text, str):
                try:
                    text = text.decode('utf-8')
                except UnicodeDecodeError:
                    errors[name]. append(_('expected UTF-8 encoding'))
        if output is not None and text:
            output[lang] = text.split(',')

    if output is None:
        return

    for lang in output:
        del extras[prefix + lang]
    data[key] = json.dumps(output)


def fluent_tags_output(value):
    """
    Return stored json representation as a multilingual dict, if
    value is already a dict just pass it through.
    """
    if isinstance(value, dict):
        return value
    return json.loads(value)
