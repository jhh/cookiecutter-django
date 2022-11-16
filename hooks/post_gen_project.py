import json
import random
import string
from pathlib import Path

DJANGO_SECRET_LENGTH = 64


def rename_env():
    p = Path(".env-template")
    return p.rename(Path(".env"))


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


def remove_tailwind_css():
    Path("{{cookiecutter.project_slug}}/static/css/base.css").unlink()
    Path("tailwind.config.js").unlink()
    Path("postcss.config.js").unlink()


def remove_missing_css():
    pass


TAILWIND_DEPS = [
    "@tailwindcss/forms",
    "autoprefixer",
    "cssnano",
    "npm-watch",
    "postcss",
    "postcss-cli",
    "prettier-plugin-tailwindcss",
    "tailwindcss",
]


def generate_package_json():
    pj_path = Path("package.json")

    with pj_path.open() as f:
        pj = json.load(f)

    if "{{cookiecutter.css_framework}}" != "Tailwind CSS":
        for dep in TAILWIND_DEPS:
            del pj["devDependencies"][dep]
        del pj["watch"]
        del pj["scripts"]

    if "{{ cookiecutter.use_htmx }}" != "y":
        del pj["devDependencies"]["htmx.org"]

    if "{{ cookiecutter.use_hyperscript }}" != "y":
        del pj["devDependencies"]["hyperscript.org"]

    with pj_path.open(mode="w") as f:
        json.dump(pj, f, indent=2)


def main():
    env_path = rename_env()
    set_django_secret_key(env_path)

    generate_package_json()

    if "{{cookiecutter.css_framework}}" != "Tailwind CSS":
        remove_tailwind_css()

    if "{{cookiecutter.css_framework}}" != "Missing CSS":
        remove_missing_css()


if __name__ == "__main__":
    main()
