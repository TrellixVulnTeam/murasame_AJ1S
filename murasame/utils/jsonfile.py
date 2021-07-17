## ============================================================================
##             **** Murasame Application Development Framework ****
##                Copyright (C) 2019-2021, Suisei Entertainment
## ============================================================================
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
## ============================================================================

"""
Utility class to help in parsing and handling JSON files.
"""

# Runtime Imports
import json
from typing import Callable

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils.aes import AESCipher
from murasame.utils.contentfile import ContentFile

class JsonFile(ContentFile):

    """Represents a single JSON file on disk. The content of the file can be
    encrypted.

    Authors:
        Attila Kovacs
    """

    def __init__(self, path: str, cb_retrieve_key: Callable = None) -> None:

        """Creates a new JsonFile instance.

        Args:
            path (str): Path to the JSON file on disk.

            cb_retrieve_key (Callable): Optional callback function that will be
                called to retrieve the key to decrypt the file.

        Authors:
            Attila Kovacs
        """

        super().__init__(path=path, cb_retrieve_key=cb_retrieve_key)

    def save_unencrypted(self, compact: bool = True) -> None:

        """Saves the content of the file unencrypted to disk.

        Args:
            compact (bool): Specifies whether or not the file should be saved
                in a compact, less readable format, or in a properly indented
                and formatted way. This has no effect on encrypted files.

        Raises:
            RuntimeError: Raised when the file cannot be saved.

        Authors:
            Attila Kovacs
        """

        # Save the file unencrypted.
        try:
            with open(self._path, 'w+') as json_file:
                if compact:
                    json.dump(self._content, json_file)
                else:
                    json.dump(self._content,
                              json_file,
                              indent=4,
                              separators=(',', ': '))
        except OSError as exception:
            raise RuntimeError(
                'Failed to save the content of JSON file to {}.'.format(
                    self._path)) from exception

    def load_unencrypted(self) -> None:

        """Try to load the file as an unencrypted JSON file.

        Raises:
            InvalidInputError: Raised when the file cannot be loaded.

            InvalidInputError: Raised when the content of the file cannot be
                parsed by the parser.

        Authors:
            Attila Kovacs
        """

        try:
            with open(self._path, 'r+') as json_file:
                # Parse the file and load the content to memory.
                self._content = json.load(json_file)
        except OSError as exception:
            self._content = None
            raise InvalidInputError(
                'Failed to read the contents of JSON file {}.'.format(
                    self._path)) from exception
        except json.JSONDecodeError as exception:
            self._content = None
            raise InvalidInputError(
                'Failed to parse the content of JSON file {}.'.format(
                    self._path)) from exception

    def save_encrypted(self, compact: bool = True) -> None:

        """Encrypt the content of the file and save it to disk.

        Args:
            compact (bool): Specifies whether or not the file should be saved
                in a compact, less readable format, or in a properly indented
                and formatted way. This has no effect on encrypted files.

        Raises:
            RuntimeError: Raised if the content of the file cannot be saved to
                disk.

        Authors:
            Attila Kovacs
        """

        # Encrypt the file before saving
        cipher = AESCipher(self._cb_retrieve_key())
        encrypted_content = cipher.encrypt(json.dumps(self._content))

        try:
            with open(self._path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_content)
        except OSError as exception:
            raise RuntimeError(
                'Failed to save the content of JSON file to {}.'.format(
                    self._path)) from exception

    def load_encrypted(self) -> None:

        """Try to load and decrypt the file.

        Raises:
            InvalidInputError: Raised when the file cannot be loaded.

            InvalidInputError: Raised when the content of the file cannot be
                parsed.

        Authors:
            Attila Kovacs
        """

        raw_content = None
        try:
            with open(self._path, 'rb') as raw_file:
                raw_content = raw_file.read()
        except OSError as exception:
            raise InvalidInputError(
                'Failed to read the file from disk: {}.'.format(
                    self._path)) from exception

        if raw_content is not None:

            # Try to load as a regular JSON file
            try:
                cipher = AESCipher(self._cb_retrieve_key())
                self._content = json.loads(
                    cipher.decrypt(raw_content))
            except json.JSONDecodeError as exception:
                raise InvalidInputError(
                    'Failed to parse the content of JSON file {}. '
                    'Either the decryption key was wrong or the file '
                    'is not a valid JSON file.'.format(self._path)) from exception
