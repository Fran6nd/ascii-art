.DEFAULT_GOAL := default

clean:
	rm -f ascii-art
default: clean
	python3 -m nuitka main.py --follow-imports -o ascii-art
install: default
	sudo mv ascii-art /usr/bin

