# Define the path to your virtual environment's python
PYTHON = ./venv/bin/python

# Now use $(PYTHON) instead of just 'python'
migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

graph:
	$(PYTHON) manage.py graph_models polls -o polls_schema.png

graph-full:
	$(PYTHON) manage.py graph_models -a -g -o full_detail_schema.png
#
dev-backend:
	$(PYTHON) manage.py runserver --noreload

test-polls:
	$(PHTHON) manage.py test polls.tests