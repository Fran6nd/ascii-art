import sys,os
import curses
import lib
import cv2

def draw_menu(stdscr):


    # Loop where k is the last character pressed
    cam = cv2.VideoCapture(0)
    #cam = cv2.VideoCapture("rtmp://192.168.1.100/live/av0")



    frame,err = cam.read()
    #if err:
    print(err, "yo", frame)



    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    stdscr.nodelay(1)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    filter = lib.videofilter()
    vf = lib.videofilter()
    while (k != ord('q')):
        ret_val, img = cam.read()
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)



        txt = vf.process_cv_image(img, (curses.COLS-1, curses.LINES)).split("\n")
        for i in range(curses.LINES):

            stdscr.addstr(i, 0, str((txt[i])))
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
