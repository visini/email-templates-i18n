import os
import uuid
from pathlib import Path

from fastapi import FastAPI, Response

from src.main import get_email_config
from src.messages import (
    EmailVerificationEmailMessage,
    PasswordResetEmailMessage,
)


def generate_previews():

    RPATH = os.getcwd() + "/tmp/preview"
    UPATH = os.getcwd() + "/utils"

    # =================================================================
    # Preview Settings

    config_path = "./src/data"
    lang_path = "./src/data/lang"
    templates_path = "./src/templates"

    dummy_variables = {
        "cta_url": "https://www.example.com/",
        "operating_system": "macOS 11.1",
        "browser_name": "Chrome 88.0",
    }

    config = get_email_config(config_path)
    for locale in config.available_locales:
        for ObjEmailMessage in [
            EmailVerificationEmailMessage,
            PasswordResetEmailMessage,
        ]:
            email_message = ObjEmailMessage(
                config_path, lang_path, templates_path, locale, dummy_variables
            ).get_message(debug=True)
            email_type = email_message.email_type

            R_RPATH = RPATH + "/" + locale + "/" + email_type
            Path(R_RPATH).mkdir(parents=True, exist_ok=True)

            with open(f"{R_RPATH}/preview.html", "w") as f:
                f.write(email_message.html)
            with open(f"{R_RPATH}/preview.txt", "w") as f:
                f.write(email_message.txt)

    # =================================================================

    app = FastAPI()

    uuid_seed = uuid.uuid4()

    @app.get("/{locale}/{email_message}/{format}")
    def preview_email_message(locale: str, email_message: str, format: str):
        with open(
            f"{RPATH}/{locale}/{email_message}/preview.{format}", "r"
        ) as f:
            html = f.read()
            return Response(content=html)

    @app.get("/")
    def index():
        with open(f"{UPATH}/preview.html", "r") as f:
            html = f.read()
            return Response(content=html)

    @app.get("/seed")
    def seed():
        return {"seed": uuid_seed}

    @app.get("/preview_config")
    def preview_config():
        return {
            "available_locales": config.available_locales,
            "available_messages": config.available_messages,
        }

    return app


app = generate_previews()
