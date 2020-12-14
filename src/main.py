import json
import logging
from functools import lru_cache

from jinja2 import Environment, FileSystemLoader, Template
from premailer import transform

# Disable warnings for premailer
# e.g., Unknown Property name. [word-break]
logging.getLogger("CSSUTILS").setLevel("CRITICAL")


class EmailConfig:
    def __init__(self, config_path: str):
        with open(f"{config_path}/global.json", "r") as f:
            self.global_variables = json.loads(f.read())
        with open(f"{config_path}/config.json", "r") as f:
            self.config = json.loads(f.read())
        self.available_locales = self.config["available_locales"]
        self.available_messages = self.config["available_messages"]


class LocalizedTemplates:
    def __init__(
        self, config_path: str, lang_path: str, templates_path: str, locale: str
    ):

        self.locale = locale
        if self.locale not in get_email_config(config_path).available_locales:
            raise Exception(f"locale '{self.locale}' is not defined!")

        self.locales = {}
        for locale in get_email_config(config_path).available_locales:
            with open(f"{lang_path}/{locale}.json", "r") as f:
                self.locales[locale] = json.loads(f.read())

        env = Environment(loader=FileSystemLoader(templates_path))
        self.templates = {}
        for template in get_email_config(config_path).available_messages:
            self.templates[template] = {
                "html": env.get_template(f"{template}.html"),
                "txt": env.get_template(f"{template}.txt"),
            }


@lru_cache
def get_email_config(config_path: str) -> EmailConfig:
    return EmailConfig(config_path)


@lru_cache
def get_all_localized_templates(
    config_path: str, lang_path: str, templates_path: str, locale: str
) -> LocalizedTemplates:
    return LocalizedTemplates(config_path, lang_path, templates_path, locale)


class EmailMessage:
    def __init__(
        self,
        config_path,
        lang_path,
        templates_path,
        email_type,
        required_variables,
        locale,
        variables,
    ):
        self.config_path = config_path
        self.lang_path = lang_path
        self.templates_path = templates_path
        self.email_type = email_type
        self.required_variables = required_variables
        self.locale = locale
        self.variables = variables

    def get_message(self, interpolate_variables_in_data=True, debug=False):

        for r in self.required_variables:
            if r not in self.required_variables:
                raise Exception(f"Required variable '{r}' is not defined!")

        self.locale_templates = get_all_localized_templates(
            self.config_path, self.lang_path, self.templates_path, self.locale
        )
        locales = self.locale_templates.locales[self.locale]
        localized = {
            **get_email_config(self.config_path).global_variables,
            "localized": {**locales["global"], **locales[self.email_type]},
            "variables": self.variables,
        }
        html = self.locale_templates.templates[self.email_type]["html"]
        txt = self.locale_templates.templates[self.email_type]["txt"]
        rendered_html = html.render(localized)
        rendered_txt = txt.render(localized)
        if interpolate_variables_in_data:
            rendered_html = Template(rendered_html).render(localized)
            rendered_txt = Template(rendered_txt).render(localized)
        self.html = transform(
            rendered_html,
            strip_important=False if debug else True,
        )
        self.txt = rendered_txt
        self.subject = self.locale_templates.locales[self.locale][
            self.email_type
        ]["subject"]

        return self
