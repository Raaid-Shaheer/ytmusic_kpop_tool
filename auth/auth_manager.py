from ytmusicapi import YTMusic
from pathlib import Path


class AuthManager:
    """
    Responsible for one thing only: providing an authenticated
    YTMusic instance to the rest of the application.
    """

    def __init__(self, credentials_path: str = "browser.json"):
        self.credentials_path = Path(credentials_path)
        self._client = None  # Lazy initialization — don't connect until needed

    def get_client(self) -> YTMusic:
        """
        Returns an authenticated YTMusic client.
        Creates it only once and reuses it (singleton pattern).
        """
        if self._client is None:
            if not self.credentials_path.exists():
                raise FileNotFoundError(
                    f"Credentials file not found at '{self.credentials_path}'.\n"
                    f"Run 'ytmusicapi browser' to generate it."
                )
            self._client = YTMusic(str(self.credentials_path))
            print(f"✅ Authenticated with YouTube Music")

        return self._client