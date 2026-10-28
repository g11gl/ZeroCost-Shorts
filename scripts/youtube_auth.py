#!/usr/bin/env python3
"""Authorize the intended YouTube channel on your own computer.

Requires a local OAuth Desktop client JSON under secrets/client_secret.json.
The two scopes allow private video upload and verification of the channel ID.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
load_dotenv(REPO_ROOT / ".env")

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pipeline.youtube_destination import verify_kids_channel

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]
SECRETS = REPO_ROOT / "secrets"


def main() -> None:
    client_secret = SECRETS / "client_secret.json"
    token_out = SECRETS / "youtube_token.json"

    if not client_secret.is_file():
        print(
            "Missing secrets/client_secret.json\n\n"
            "1. Enable YouTube Data API v3:\n"
            "   https://console.cloud.google.com/apis/library/youtube.googleapis.com\n"
            "2. Create an OAuth client ID for a Desktop application.\n"
            "3. Save the downloaded JSON as secrets/client_secret.json.\n"
        )
        sys.exit(1)

    print("Opening browser for Google OAuth…")
    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret), SCOPES)
    creds = flow.run_local_server(port=0)

    # Do not retain or export a token that points at another channel.
    youtube = build("youtube", "v3", credentials=creds)
    verify_kids_channel(youtube.channels().list(part="id", mine=True).execute())

    SECRETS.mkdir(parents=True, exist_ok=True)
    token_out.write_text(creds.to_json(), encoding="utf-8")
    print(f"\nVerified kids channel; OAuth token saved to {token_out}")

    token_data = json.loads(creds.to_json())
    print("\nAdd these as repository GitHub Actions secrets (do not commit them):")
    print(f"  YT_REFRESH_TOKEN = {token_data.get('refresh_token', '???')}")
    print(f"  YT_CLIENT_ID = {token_data.get('client_id', '???')}")
    print(f"  YT_CLIENT_SECRET_VALUE = {token_data.get('client_secret', '???')}")
    print("Never paste these values into public files or chat.")


if __name__ == "__main__":
    main()
