import os
import random
import string
from pathlib import Path

DJANGO_SECRET_LENGTH = 64

REMOVE_PATHS = [
    '{% if cookiecutter.css_framework != "tailwind" %}tailwind.config.js{% endif %}',
    '{% if cookiecutter.css_framework != "tailwind" %}{{ cookiecutter.project_slug }}/static/css/base.css{% endif %}',
    "{{ cookiecutter.project_slug }}/templates/index.bootstrap.html",
    "{{ cookiecutter.project_slug }}/templates/index.none.html",
    "{{ cookiecutter.project_slug }}/templates/index.tailwind.html",
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
        path = path.strip()
        if path and os.path.exists(path):
            os.unlink(path) if os.path.isfile(path) else os.rmdir(path)


def set_index_html():
    src = Path(
        "{{ cookiecutter.project_slug }}/templates/index.{{ cookiecutter.css_framework }}.html"
    )
    dest = Path("{{ cookiecutter.project_slug }}/templates/index.html")
    src.rename(dest)


def main():
    env_path = rename_env()
    set_django_secret_key(env_path)
    create_empty_js_dir()
    set_index_html()
    remove_paths()  # must come after set_index_html


if __name__ == "__main__":
    main()
