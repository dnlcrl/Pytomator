# Pytomator

## Vision-based Automation Python Module for OS X


This Python module make use of [OpenCV][1], [NumPy][2] and [Quartz][3] to control mouse and keyboard events automatically, [CV] [4]'ing your OS X screen.

## Pre-requisites

In order to compile Pytomator you must have OpenCV installed on your machine.

### Install [OpenCV](http://opencv.org/) (with [Homebrew](http://brew.sh/))
Run 

	$ brew install opencv

Then follow the instructions given by Homebrew.

## Installation

At the moment you can download and copy all the files in your project folder and add this lines to your file if you want only match templates and/or control the mouse
	
	from pytomator import *
	
Add also this line if you want to control the keyboard too

	from keyboard import PyKeyboard

## Basic Usage

You must provide an image to the match function, which return the center coordinates of the matched area, you can then click, drag, or move the mouse at such coordinates. 

	x, y = match(template_path)
    mouseclick_visive(x, y)

You can control key pressing events in this way

	ch = 'p'
    k = PyKeyboard()
    k.press_key(ch)
    k.release_key(ch)

## Notes

+ If you are wondering why the big words in my [code](https://github.com/danieleciriello/Pytomator/blob/master/pytomator.py), read [this](http://ergoemacs.org/emacs/proper_way_to_use_Sublime_Text_minimap.html).
+ Thanks to [SavinaRoja](https://github.com/SavinaRoja) for base.py and keyboard.py ([originally](https://github.com/SavinaRoja/PyUserInput) mac.py)
+ Suggestions are welcome

[1]: http://opencv.org/ "http://opencv.org/"
[2]: http://www.numpy.org/ "http://www.numpy.org/"
[3]: https://developer.apple.com/library/mac/documentation/GraphicsImaging/Reference/Quartz2D_Collection/_index.html "https://developer.apple.com/library/mac/documentation/GraphicsImaging/Reference/Quartz2D_Collection/_index.html"
[4]: http://en.wikipedia.org/wiki/Computer_vision "Computer Vision"