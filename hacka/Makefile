run:
	python3 ./src/gtk-gui/flix-with-friends

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +
	-rm -rf '__pycache__'

db:
	python3 Database.py

requirements:
	find . -name 'requirements.txt' -exec rm --force {} +
	pip3 freeze>requirements.txt
