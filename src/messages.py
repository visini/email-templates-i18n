from src.main import EmailMessage


class EmailVerificationEmailMessage(EmailMessage):
    def __init__(self, config_path, lang_path, email_path, locale, variables):
        self.email_type = "email_verification"
        self.required_variables = ["cta_url"]
        super().__init__(
            config_path,
            lang_path,
            email_path,
            self.email_type,
            self.required_variables,
            locale,
            variables,
        )


class PasswordResetEmailMessage(EmailMessage):
    def __init__(self, config_path, lang_path, email_path, locale, variables):
        self.email_type = "password_reset"
        self.required_variables = [
            "cta_url",
            "operating_system",
            "browser_name",
        ]
        super().__init__(
            config_path,
            lang_path,
            email_path,
            self.email_type,
            self.required_variables,
            locale,
            variables,
        )
