VENV_DIR = .venv

all: clean venv resources

venv:
	@virtualenv --python=python3 --system-site-packages --prompt="(py3qt4)" $(VENV_DIR)
	@bash -c 'source ./'$(VENV_DIR)'/bin/activate && pip install pylint pytz simplejson'

resources:
	@LANG=C pyrcc4 -o resources.py -py3 resources.qrc

clean:
	@rm -rf $(VENV_DIR)
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name '*.py[co]' -exec rm -f {} \;

