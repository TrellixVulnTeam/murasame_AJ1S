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
Contains the implementation of the HostLocation class.
"""

# Runtime Imports
import os
import tarfile
import shutil
import uuid
from urllib.error import ContentTooShortError

# Dependency Imports
import geoip2
import geoip2.database
import wget

# Murasame Imports
from murasame.exceptions import InvalidInputError
from murasame.utils import GeoIP
from murasame.logging import LogWriter

PACKAGE_DOWNLOAD_LOCATION = '/tmp'

class HostLocation(LogWriter):

    """
    Utility class to determine the location of the host based on it's GeoIP
    data.

    At the moment this class uses MaxMind's GeoIP 2 Lite database to determine
    the location of a given IP address.

    Authors:
        Attila Kovacs
    """

    @property
    def Continent(self) -> str:

        """
        The continent where the IP address is located.

        Authors:
            Attila Kovacs
        """

        return self._continent

    @property
    def Country(self) -> str:

        """
        The country where the IP address is located.

        Authors:
            Attila Kovacs
        """

        return self._country

    @property
    def City(self) -> str:

        """
        The city where the IP address is located.

        Authors:
            Attila Kovacs
        """

        return self._city

    @property
    def Location(self) -> tuple:

        """
        The geographical location of the IP address represented as latitude and
        longitude.

        Authors:
            Attila Kovacs
        """

        return self._location

    @property
    def PostalCode(self) -> str:

        """
        The postal code where the IP address is located.

        Authors:
            Attila Kovacs
        """

        return self._postal_code

    def __init__(
            self,
            public_ip: str,
            database_path: str,
            geoip_license_key: str = None) -> None:

        """
        Creates a new HostLocation instance.

        Args:
            public_ip:          The public IP of the host.
            database_path:      Path to the diretory where the GeoIP database
                                is located.
            geoip_license_key:  The license key to use when downloading the
                                GeoIP database.

        Raises:
            InvalidInputError:  Raised if the GeoIP database was not found.

        Authors:
            Attila Kovacs
        """

        super().__init__(channel_name='murasame.pal', cache_entries=True)

        # The continent where the IP address is located
        self._continent = 'UNKNOWN'

        # The country where the IP address is located
        self._country = 'UNKNOWN'

        # The city where the UP address is located
        self._city = 'UNKNOWN'

        # The geographical coordinates of the IP address
        self._location = (0, 0)

        # The postal code where the IP address is located
        self._postal_code = 'UNKNOWN'

        self._identify_location(public_ip=public_ip,
                                database_path=database_path,
                                geoip_license_key=geoip_license_key)

    def _identify_location(
            self,
            public_ip: str,
            database_path: str,
            geoip_license_key: str = None) -> None:

        """
        Executes the host location logic.

        Args:
            public_ip:          The public IP of the host.
            database_path:      Path to the diretory where the GeoIP database
                                is located.
            geoip_license_key:  The license key to use when downloading the
                                GeoIP database.

        Authors:
            Attila Kovacs
        """

        if public_ip == 'UNKNOWN':
            self.error(
                'Unknown public IP has been provided, cannot determine'
                'location.')
            return

        full_path = os.path.abspath(os.path.expanduser(
            f'{database_path}/GeoLite2-City.mmdb'))
        self.debug(f'Loading GeoIP database from {full_path}')

        if not os.path.isfile(full_path):
            if geoip_license_key is not None:

                # Attempt to download the database
                update_link = f'https://download.maxmind.com/app/geoip_'\
                    f'download?edition_id=GeoLite2-City&license_key='\
                    f'{geoip_license_key}&suffix=tar.gz'

                # Use a random generated UUID as a temporary filename for the
                # downloaded GeoIP database to avoid it being used as a
                # potential attack vector by forcing the application to open a
                # file with malicious content if the downloaded file has been
                # compromised.
                package_temp_name = str(uuid.uuid4())
                package_filename = f'{PACKAGE_DOWNLOAD_LOCATION}/{package_temp_name}.tar.gz'

                # Download the update package
                try:
                    wget.download(url=update_link,
                                  out=package_filename)
                except ContentTooShortError as error:
                    raise RuntimeError(
                        'Failed to download GeoIP database.') from error

                # Extract the update package
                tar = tarfile.open(package_filename)
                tar.extractall(path=PACKAGE_DOWNLOAD_LOCATION,
                               members=GeoIP._find_mmdb(tar))
                tar.close()

                # Move the database to the requested location
                shutil.move(src=f'{PACKAGE_DOWNLOAD_LOCATION}/GeoLite2-City.mmdb',
                            dst=f'{database_path}/GeoLite2-City.mmdb')

                # Delete the update package
                os.remove(package_filename)
            else:
                raise InvalidInputError('GeoIP database was not found.')

        response = None

        reader = geoip2.database.Reader(full_path)
        try:
            self.debug(f'Trying to locate public IP ({public_ip}) in the '
                       f'GeoIP database.')
            response = reader.city(public_ip)
        except geoip2.errors.AddressNotFoundError:
            # IP address not found
            self.warning(f'Public IP ({public_ip}) was not found in the '
                         f'GeoIP database.')

        if response:
            self._continent = response.continent.name
            self._country = response.country.name
            self._city = response.city.name
            self._postal_code = response.postal.code
            self._location = (
                response.location.latitude,
                response.location.longitude)
            self.debug(f'Location of public IP {public_ip}: {self._continent} '
                       f'- {self._country} - {self._city} '
                       f'({self._postal_code})')
