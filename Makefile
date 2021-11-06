.DEFAULT_GOAL := default

clean:
	rm -f ascii-art
	rm -f ascii-art-video
default: clean
	python3 -m nuitka main.py --follow-imports -o ascii-art
video: clean
	python3 -m nuitka main1.py  --follow-imports --nofollow-import-to cv2 -o video
install: default
	sudo mv ascii-art /usr/bin

