import boto3
from botocore.exceptions import ClientError

from src.messages import EmailVerificationEmailMessage

config_path = "./src/data"
lang_path = "./src/data/lang"
templates_path = "./src/templates"

# Message config
locale = "en-US"
variables = {"cta_url": "https://www.example.com/"}
message = EmailVerificationEmailMessage(
    config_path, lang_path, templates_path, locale, variables
)

#  Application config
SENDER = "Sender Name <sender@example.com>"
RECIPIENT = "recipient@example.com"
CONFIGURATION_SET = "ConfigSet"
AWS_REGION = "us-west-2"

client = boto3.client("ses", region_name=AWS_REGION)

try:
    response = client.send_email(
        Destination={
            "ToAddresses": [RECIPIENT],
        },
        Message={
            "Body": {
                "Html": {"Charset": "UTF-8", "Data": message.html},
                "Text": {"Charset": "UTF-8", "Data": message.txt},
            },
            "Subject": {"Charset": "UTF-8", "Data": message.subject},
        },
        Source=SENDER,
        ConfigurationSetName=CONFIGURATION_SET,
    )

except ClientError as e:
    print(e.response["Error"]["Message"])
else:
    print("Email sent! Message ID:"),
    print(response["MessageId"])
