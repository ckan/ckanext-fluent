import ckan.plugins as p
from ckan.plugins.toolkit import add_template_directory, h

from ckanext.fluent import validators, helpers


class FluentPlugin(p.SingletonPlugin):
    p.implements(p.IValidators)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        """
        We have some form snippets that support ckanext-scheming
        """
        add_template_directory(config, 'templates')

    def get_helpers(self):
        template_helpers = {
            'fluent_form_languages': helpers.fluent_form_languages,
            'fluent_form_label': helpers.fluent_form_label,
        }
        if 'truncate' not in h:
            from ckan.lib.helpers import truncate
            template_helpers['truncate'] = truncate
        return template_helpers

    def get_validators(self):
        return {
            'fluent_text': validators.fluent_text,
            'fluent_text_output':
                validators.fluent_text_output,
            'fluent_tags': validators.fluent_tags,
            'fluent_tags_output':
                validators.fluent_tags_output,
            'fluent_core_translated_output':
                validators.fluent_core_translated_output,
            }
