ckanext-fluent
==============

This extension provides a way to store and return multilingul
fields in CKAN datasets, resources, organizations and groups.

Add the `fluent` plugin to your ckan.plugins configuration
settings and use ckanext-scheming or a custom form plugin to
use the provided validators to store multilingual text in
extra fields.

The easiest way to use fluent multilingual text fields is with
[ckanext-scheming](https://github.com/open-data/ckanext-scheming/).
Add `ckanext.fluent:presets.json` to your scheming.presets
configuration settings:

```json
scheming.presets = ckanext.scheming:presets.json
                   ckanext.fluent:presets.json
```

A fluent multilingual field in a scheming schema
will look something like::

```json
{
  "field_name": "books",
  "preset": "fluent_text",
  "label": {
    "en": "Books",
    "fr": "Livres"
  },
  "form_languages": ["en", "fr"]
}
```

This new extra field "books" will appear as multiple fields in the
dataset form, one for each language specified in `form_languages`
by the [form snippet](ckanext/fluent/templates/scheming/form_snippets/fluent_text.html).

![Example of fluent form snippet](docs/multilingual-form.png)

When the dataset is accessed from the API the language values appear
and are updated as an object, eg.:

```json
{
  "...": "...",
  "books": {
    "en": "Franklin",
    "fr": "Benjamin"
  },
  "...": "..."
}
```
## Using fluent with core fields ##

Fluent should not be directly used on ckan core fields such as `title` and `notes`.
To use fluent to translate core fields, you should use a field with the `_translated`
suffix appended to the core field name (e.g. `title_translated`) and use the `fluent_core_translated`
preset. By doing so, the translated version of the field is stored in the field with the
`_translated` suffix while the core field displays the value for the site's default language.

```json

{
  "field_name": "title_translated",
  "preset": "fluent_core_translated",
  "label": {
    "en": "Franklin",
    "fr": "Benjamin"
  }
}
```
