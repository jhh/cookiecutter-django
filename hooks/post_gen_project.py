import json
import os
import random
import string
from pathlib import Path

DJANGO_SECRET_LENGTH = 64

REMOVE_PATHS = [
    '{% if cookiecutter.use_tailwind != "y" %}tailwind.config.js{% endif %}',
]


def rename_env():
    p = Path("envrc-template")
    return p.rename(Path(".envrc"))


def generate_secret_key():
    symbols = []
    symbols += string.digits
    symbols += string.ascii_letters
    return "".join([random.choice(symbols) for _ in range(DJANGO_SECRET_LENGTH)])


def set_django_secret_key(env_path):
    secret_key = generate_secret_key()
    with env_path.open(mode="r+") as f:
        file_contents = f.read().replace("!!!SET DJANGO_SECRET_KEY!!!", secret_key)
        f.seek(0)
        f.write(file_contents)
        f.truncate()


def create_empty_js_dir():
    path = Path("{{ cookiecutter.project_slug}}/static/js")
    path.mkdir()


def remove_paths():
    for path in REMOVE_PATHS:
        path = Path(path.strip())
        if path.exists():
            path.unlink() if path.is_file() else path.rmdir()


def main():
    env_path = rename_env()
    set_django_secret_key(env_path)
    create_empty_js_dir()
    remove_paths()


if __name__ == "__main__":
    main()
