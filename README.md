# Heimdall
## Description
Heimdall is an open-source tool, written in Python, that searches a text for sequences written in other languages than the main one. Heimdall's roots in [historical linguistics](https://www.uantwerpen.be/en/projects/mind-bending-grammars/) are reflected in the language models it is shipped with: its three default languages are medieval Latin, Early Modern French and Early Modern English. The tool is compatible with plain text files as well as xml-files. In the first case, it simply outputs a list of all foreign passages. In the second, it also allows you to tag the foreign passages directly in the input documents.

Heimdall comes in two versions. There is a version with a graphical user interface, which implements the basic functionalities and allows users without programming skills to quickly parse their input files. The alternative is the command-line version, which is less user-friendly, but offers more flexibility. Apart from tagging files and tweaking the basic parameter settings, the command-line tool lets you create new language models (provided you have a sufficiently large corpus of the target language) and change the parameter settings more drastically. As Heimdall is completely open source, users who feel comfortable with Python are encouraged to amend the tagging algorithm to improve overall performance, or optimize the tool for their own research endeavours.

If you want to get started quickly, you'll find the installation guide and basic usage instructions below. For more elaborate usage instructions, a discussion of the implemented tagging algorithm, or suggestions to improve and expand the tagger, we kindly refer you to our Wiki.

## Installation guide
### Windows and Mac
If you're on Mac or Windows and want to use the tool via its graphical interface, you don't need to install anything. Just download the zip-folder, unzip it, doubleclick the executable ("heimdall.exe" for Windows, "heimdall.app" for Mac), and you're good to go.

### Unix
If you're on a Unix-based platform or if you want to use the tool from the command line, you'll have to download the source code and some of the dependencies.
First of all, make sure you've got a working installation of Python 3. If you don't have Python on your device already, you can download the most recent version from [their website](https://www.python.org/downloads/).

## Basic usage instructions


## Credits

Heimdall was developed by [Sara Budts](https://www.uantwerpen.be/nl/personeel/sara-budts/), for and in collaboration with the [Mind Bending Grammars team](https://www.uantwerpen.be/en/projects/mind-bending-grammars/) at the University of Antwerp. Don't hesitate to get in touch with us if you have any comments, questions, suggestions, or other kinds of feedback. The link attached to our names will lead you to our university website, where you'll find our contact details.
