"""Guard against uploading children's lessons to the wrong YouTube channel."""

KIDS_CHANNEL_ID = "UCp54Cb0oNUWfuyf39tS1rCA"  # حروفف والوانن (@HurooffAlwann)


def verify_kids_channel(channel_response: dict) -> None:
    """Refuse a kids upload unless OAuth belongs to the intended channel."""
    found_ids = [item.get("id") for item in channel_response.get("items", [])]
    if found_ids != [KIDS_CHANNEL_ID]:
        raise RuntimeError(
            "YouTube OAuth is not authorized for the children's channel "
            f"{KIDS_CHANNEL_ID} (@HurooffAlwann). "
            "Select that channel during OAuth authorization and refresh the GitHub token. "
            f"Authenticated channel IDs: {found_ids!r}"
        )
