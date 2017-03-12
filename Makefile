run:
	python3 flix-with-friends

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +
	-rm -rf '__pycache__'

requirements:
	find . -name 'requirements.txt' -exec rm --force {} +
	pip3 freeze>requirements.txt
