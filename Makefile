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

WORKSPACE_DIRECTORY =  ~/.murasame
VIRTUALENV_DIRECTORY = ./.env

configure:
	echo "Creating workspace directories..."
	mkdir -p $(WORKSPACE_DIRECTORY)
	mkdir -p $(WORKSPACE_DIRECTORY)/testfiles
	mkdir -p $(WORKSPACE_DIRECTORY)/logs
	mkdir -p $(WORKSPACE_DIRECTORY)/logs/unittest
	echo ""

	echo "Creating virtual environment in ./.env..."
	virtualenv --python=python3.8 $(VIRTUALENV_DIRECTORY)
	echo ""

	echo "Installing requirements inside the virtual environment..."
	source $(VIRTUALENV_DIRECTORY)/bin/activate; \
	pip install -r requirements-dev.txt; \
	pip install -r requirements.txt;
	echo ""

install:
	echo "Uninstalling previous version..."
	pip uninstall -y murasame
	echo ""

	echo "Installing current version..."
	pip install ./dist/murasame-0.1.0-py3-none-any.whl
	echo ""

build:
	echo "Executing project build..."
	./scripts/build
	echo ""

documentaiton:
	echo "Building project documentation..."
	sphinx-build -E -a -b html ./documentation/ ./dist/documentation/
	echo ""

unittest:
	echo "Executing unit tests..."
	pytest -v --html=$(WORKSPACE_DIRECTORY)/logs/unittest/report.html --self-contained-html
	echo ""

lint:
	echo "Executing linter..."
	pylint --rcfile=./.pylintrc --exit-zero ./murasame
	echo ""

coverage:
	echo "Measuring unit test coverage..."
	coverage run -m pytest -vv --html=$(WORKSPACE_DIRECTORY)/logs/unittest/report.html --self-contained-html
	coverage report
	coverage html
	echo ""

.PHONY: unittest build