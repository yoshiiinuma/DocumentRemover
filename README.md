# DocumentRemover

# How to install (new)
```bash
$ pip install pipenv
$ cd DocumentRemover
$ pipenv install --dev
```

# How to generate requirements.txt
```bash
# For Production
$ pipenv lock -r > requirements.txt

# For development
$ pipenv run pip freeze > requirements.txt
```

# How to set up the application running environment
```bash
# Run this command before running the app or tests
$ pipenv shell
```

# How to test
```bash
$ pipenv shell
$ pytest
```

# How to run
```bash
$ pipenv shell
$ python bin/main.py config/config.json
```

# How to use pylint
```bash
$ pipenv shell
$ pylint path-to-file
```

# How to deploy to Google Functions
