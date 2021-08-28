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
Contains the unit tests of GRPCServer class.
"""

# Runtime Imports
import os
import sys

# Dependency Imports
import pytest

# Fix paths to make framework modules accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Murasame Imports
from murasame.pal.networking.grpcserver import GRPCServer
from murasame.pal.networking.grpcservertypes import GRPCServerTypes

class TestGRPCServer:

    """
    Contains the unit tests for the GRPCServer class.

    Authors:
        Attila Kovacs
    """

    def test_creation_of_insecure_server(self):

        """
        Tests that an insecure gRPC server can be created.

        Authors:
            Attila Kovacs
        """

        sut = GRPCServer(port=12345,
                         server_type=GRPCServerTypes.INSECURE)

        assert sut is not None
