import boto3


def translate_text(text, source, target):
    """Translate text from source to target language"""

    client = boto3.client("translate")
    result = client.translate_text(
        Text=text, SourceLanguageCode=source, TargetLanguageCode=target
    )
    return (
        result["TranslatedText"],
        result["SourceLanguageCode"],
        result["TargetLanguageCode"],
    )


def list_languages():
    """List available languages"""

    client = boto3.client("translate")
    result = client.list_languages()
    return result["Languages"]
