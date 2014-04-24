# Pytomator

## Vision-based Automation Python 2.7 Module for OS X


This Python module make use of [OpenCV][1], [NumPy][2] and [Quartz][3] to control mouse and keyboard events automatically, [CV] [4]'ing your OS X screen.

## Pre-requisites

In order to compile Pytomator you must be on OS X 10.8 or higher and have OpenCV installed on your machine.

### Install [OpenCV](http://opencv.org/) (with [Homebrew](http://brew.sh/))
Run 

	$ brew install opencv

Then follow the instructions given by Homebrew.

## Installation

To install pytomator run

	$ sudo pip install git+git://github.com/danieleciriello/Pytomator


## Basic Usage

Add this lines to your file to add pytomator to your Python module

	from pytomator import pytomator

You must provide an image to the match function, which return the center coordinates of the matched area, you can then click, drag, or move the mouse at such coordinates. 

	x, y = pytomator.match(template_path)
    pytomator.mouseclick_visive(x, y)

You can control key pressing events in this way

	for c in 'spam':
	    pytomator.keyboard.press_key(c)
	    pytomator.keyboard.release_key(c)

## License

Copyright (c) 2014 Daniele Ciriello

See [LICENSE.txt](https://github.com/danieleciriello/Pytomator/blob/master/LICENSE.txt) for license information.


## Notes

+ Thanks to [SavinaRoja](https://github.com/SavinaRoja) for base.py and keyboard.py ([originally](https://github.com/SavinaRoja/PyUserInput) mac.py)
+ Suggestions are welcome

[1]: http://opencv.org/ "http://opencv.org/"
[2]: http://www.numpy.org/ "http://www.numpy.org/"
[3]: https://developer.apple.com/library/mac/documentation/GraphicsImaging/Reference/Quartz2D_Collection/_index.html "https://developer.apple.com/library/mac/documentation/GraphicsImaging/Reference/Quartz2D_Collection/_index.html"
[4]: http://en.wikipedia.org/wiki/Computer_vision "Computer Vision"