.ONESHELL:

VENV_PATH = venv
PREFERRED_SHELL = /usr/bin/zsh

encrypt-secrets:
	@echo "encrypting secrets"
	sops -e env.json > env.json.enc
	mv env.json.enc env.json

run-env:
	@echo "loading the environment"
	source $(VENV_PATH)/bin/activate
	sops exec-env env.json $(PREFERRED_SHELL)


