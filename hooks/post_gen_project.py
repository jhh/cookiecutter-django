import random
import string
from pathlib import Path

DJANGO_SECRET_LENGTH = 64


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


def main():
    env_path = rename_env()
    set_django_secret_key(env_path)
    print("Next...")
    print("  $ cd {{ cookiecutter.project_slug }}")
    print("  $ direnv allow")
    print("  $ git init && git add .")
    print("  $ just init")


if __name__ == "__main__":
    main()
