check: pre-commit
    pre-commit run --all-files
# install pre-commit hooks
pre-commit:
    pre-commit install --install-hooks
    pre-commit autoupdate