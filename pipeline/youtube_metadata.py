"""Pure metadata builder for YouTube uploads; safe to test without credentials."""


def build_upload_body(
    title: str,
    description: str,
    *,
    privacy_status: str = "private",
    category_id: str = "24",
    made_for_kids: bool = False,
) -> dict:
    """Create explicit video metadata; the audience flag must never be omitted."""
    return {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": made_for_kids,
        },
    }
