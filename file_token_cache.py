import os
from msal import SerializableTokenCache


class FileTokenCache(SerializableTokenCache):
    def __init__(self, cache_file="token_cache.json"):
        """
        Initializes a new instance of the FileTokenCache class (which inherits from SerializableTokenCache).

        Args:
            cache_file (str): The path to the token cache file. Defaults to "token_cache.json".

        Returns:
            None
        """
        super(FileTokenCache, self).__init__()
        self.cache_file = cache_file
        if os.path.exists(self.cache_file):
            self.deserialize(open(self.cache_file, "r").read())

    def save_cache(self):
        """
        Saves the current token cache to the file.

        Args:
            None

        Returns:
            None
        """
        with open(self.cache_file, "w") as f:
            f.write(self.serialize())

    def load_cache(self):
        """
        Loads the token cache from the file.

        Args:
            None

        Returns:
            None
        """
        if os.path.exists(self.cache_file):
            self.deserialize(open(self.cache_file, "r").read())
