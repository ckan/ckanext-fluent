import pytest

from ckan.plugins.toolkit import missing

from ckanext.fluent.validators import (
    fluent_core_translated_output,
    fluent_text,
    fluent_text_output,
    fluent_tags,
    fluent_tags_output,
)

def test_text():
    txt = fluent_text(
        {'required': True},
        {'form_languages': ['en', 'fr']}
    )

    data = {('field',): {'en': 'hello', 'fr': 'bonjour'}}
    errors = {('field',): []}

    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {('field',): '{"en": "hello", "fr": "bonjour"}'}

    # accept JSON-encoded input too
    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {('field',): '{"en": "hello", "fr": "bonjour"}'}

    data = {
        ('__extras',): {'field-en': 'hello', 'field-fr': 'bonjour'},
        ('field',): missing,
    }
    errors = {('field',): []}
    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {
        ('__extras',): {},
        ('field',): '{"en": "hello", "fr": "bonjour"}',
    }

def test_text_one_missing_required():
    txt = fluent_text(
        {'required': True},
        {'form_languages': ['en', 'fr']}
    )

    data = {('field',): {'en': 'hello'}}
    errors = {('field',): []}

    txt(('field',), data, errors, {})
    assert errors == {('field',): ['Required language "fr" missing']}
    assert data == {('field',): {'en': 'hello'}}

    errors = {('field',): []}
    data = {('field',): '{"en": "hello"}'}

    txt(('field',), data, errors, {})
    assert errors == {('field',): ['Required language "fr" missing']}
    assert data == {('field',): '{"en": "hello"}'}

    data = {
        ('__extras',): {'field-fr': 'bonjour'},
        ('field',): missing,
    }
    errors = {('field',): []}
    txt(('field',), data, errors, {})
    assert errors == {('field-en',): ['Missing value'], ('field',): []}
    assert data == {
        ('__extras',): {'field-fr': 'bonjour'},
        ('field',): missing,
    }

def test_text_one_missing_not_required():
    txt = fluent_text(
        {},
        {'form_languages': ['en', 'fr']}
    )

    data = {('field',): {'en': 'hello'}}
    errors = {('field',): []}

    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {('field',): '{"en": "hello"}'}

    # accept JSON-encoded input too
    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {('field',): '{"en": "hello"}'}

    data = {
        ('__extras',): {'field-fr': 'bonjour'},
        ('field',): missing,
    }
    errors = {('field',): []}
    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {
        ('__extras',): {},
        ('field',): '{"fr": "bonjour"}',
    }

def test_text_all_missing():
    txt = fluent_text(
        {},
        {'form_languages': ['en', 'fr']}
    )

    data = {('field',): missing}
    errors = {('field',): []}

    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {('field',): '{}'}

    # accept JSON-encoded {} input
    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {('field',): '{}'}

    # actual {} input too
    data = {('field',): {}}
    txt(('field',), data, errors, {})
    assert errors == {('field',): []}
    assert data == {('field',): '{}'}

def test_core_translated_output():
    fcto = fluent_core_translated_output(
        {'field_name': 'foo_translated'},
        {}
    )
    data = {
        ('foo_translated',): {'en': 'hello'},
        ('foo',): None,
    }

    fcto(('foo_translated',), data, {}, {})
    assert data == {
        ('foo_translated',): {'en': 'hello'},
        ('foo',): 'hello',
    }

def test_text_output():
    assert fluent_text_output({'a': 'b'}) == {'a': 'b'}
    assert fluent_text_output('{"a": "b"}') == {'a': 'b'}
    assert fluent_text_output('hello') == {'en': 'hello'}

def test_tags_output():
    assert fluent_tags_output({'a': 'b'}) == {'a': 'b'}
    assert fluent_tags_output('{"a": "b"}') == {'a': 'b'}
