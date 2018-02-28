# falconer

## Quickstart

`git clone https://github.com/wsz/falconer.git`

`cd falconer/`

`mkvirtualenv -a ${PWD} -r requirements/development.txt --python=python3 falconer`

`ln --force --symbolic ${PWD}/hooks/postactivate.sh ${VIRTUAL_ENV}/${VIRTUALENVWRAPPER_ENV_BIN_DIR}/postactivate`

`ln --force --symbolic ${PWD}/hooks/predeactivate.sh ${VIRTUAL_ENV}/${VIRTUALENVWRAPPER_ENV_BIN_DIR}/predeactivate`

`alembic upgrade head`

Get the sample data at <https://drive.google.com/file/d/1-2lchmUS8HDswucYg8WvWnJtLOCCgN08/view?usp=sharing>

`tar -zxvf data.tar.gz`

`python falconer/commands/load_data.py`

`gunicorn --reload falconer.app`

