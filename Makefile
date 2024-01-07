# Settings
# - Variables
PYVERS = python3.12
VENV = ./.venv
REQUIREMENTS = ./requirements.txt

# - Parameters
ACTIVE = . ./$(VENV)/bin/activate
MAIN_FILE = bot.py

# Rules
# - Mandatory
.PHONY: all run help help-md autophony venv freeze info clean

all: help 

# - Simple Workflow
run: ## Runs the Bot's server
	@$(ACTIVE) && python $(MAIN_FILE)

# - Misc
help: ## Show this help.
	@grep "##" $(MAKEFILE_LIST) | grep -v "grep" | sed 's/:.*##\s*/:@\t/g' | column -t -s "@"

help-md: ## Show this help but in a markdown styled way. This can be used when updating the Makefile to generate documentation and simplify README.md's 'Make rules' section update.
	@grep "##" $(MAKEFILE_LIST) | grep -v "grep" | sed -E 's/([^:]*):.*##\s*/- ***\1***:@\t/g' | column -t -s "@"

autophony: ## Generate a .PHONY rule for your Makefile using all rules in the Makefile(s).
	@grep -oE "^[a-zA-Z-]*\:" $(MAKEFILE_LIST) | sed "s/://g" | xargs echo ".PHONY:"

# - Utils
venv: ## Generate a Python Virtual Environnement and install all needed packages.
	@$(PYVERS) -m venv $(VENV)
	@$(ACTIVE) && pip install --upgrade pip setuptools wheel
	@$(ACTIVE) && pip install -r $(REQUIREMENTS)

freeze: ## Freeze all the packages into the files used to create the virtual environnement.
	@$(ACTIVE) && pip freeze > $(REQUIREMENTS)

info: ## Display information about the Virtual Environnement.
	@printf "Using Virtual Environnement at '$(VENV)' with " && $(ACTIVE) && python --version

clean: ## Clean all the generated files and folders.
	@find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
