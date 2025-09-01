# Run the app

```sh
# Don't forget to activate virtual envirnoment
python main.py
```

# Adding Packages to pyproject.toml

```sh
uv add <package-name>
```

# Detect schema/ Generate migrations changes

```sh
alembic revision --autogenerate
```

# run migrations

```sh
alembic upgrade head
```

# Freeze env in requirments.txt file

```sh
uv pip compile pyproject.toml -o requirements.txt
```

# Download optional/dev deps

```sh
uv sync --extra dev
```

# run all tests

```sh
pytest
```
