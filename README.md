# Heimdall
## What's it for?
Heimdall is an open-source tool, written in Python, that searches a text for sequences written in other languages than the main one. Heimdall's roots in [historical linguistics](https://www.uantwerpen.be/en/projects/mind-bending-grammars/) are reflected in the language models it is shipped with: its three default languages are medieval Latin, Early Modern French and Early Modern English. The tool is compatible with plain text files as well as xml-files. In the first case, it simply outputs a list of all foreign passages. In the second, it also allows you to tag the foreign passages directly in the input documents.

Heimdall comes in two versions. There is a version with a graphical user interface, which implements the basic functionalities and allows users without programming skills to quickly parse their input files. The alternative is the command-line version, which is less user-friendly, but offers more flexibility. Apart from tagging files and tweaking the basic parameter settings, the command-line tool lets you create new language models (provided you have a sufficiently large corpus of the target language) and change the parameter settings more drastically. As Heimdall is completely open source, users who feel comfortable with Python are encouraged to amend the tagging algorithm to improve overall performance, or optimize the tool for their own research endeavours. 

Please note that Heimdall is not the result of intensive research on strategies to extract foreign language sequences. From an algorithmic perspective, the tool is even remarkably simple. Therefore, we'd like to stress that Heimdall by no means implements the best algorithm around. That's simply not what it's optimized for. What it does excel at, however, is user-friendliness, availability, transparency, and extensibility to different input formats, different languages, and even different tagging algorithms. If you'd like to contribute to the algorithmic aspect, we'd love to hear from you. You'll find a couple of possible extensions in our [Wiki](https://github.com/srbdts/heimdall/wiki/7.-Future-Improvements-(by-you%3F)) - these are obvious improvents that we haven't got around to ourselves - but feel free to suggest your own upgrades.

If you want to get started quickly, you'll find the installation guide and basic usage instructions below. For more elaborate usage instructions, a discussion of the implemented tagging algorithm, or suggestions to improve and expand the tagger, we kindly refer you to the elaborate documentation in our [Wiki](https://github.com/srbdts/heimdall/wiki/).

If you've used Heimdall in your research, please cite the tool via it's official doi: 10.5281/zenodo.3621420.

## Installation guide
### Windows and Mac - Graphical interface
If you're on Mac or Windows and want to use the tool via its graphical interface, you don't need to install anything. Just download the zip-folder, unzip it, doubleclick the executable ("heimdall.exe" for Windows, "heimdall.app" for Mac), and you're good to go.

### Windows and Mac - Command line interface
If you'd like use the command line interface rather than the graphical user interface, if you want to add new languages or play around with the code yourself, you'll need to take the same steps as the Unix users below.

### Unix
If you're on a Unix-based platform or if you want to use the tool from the command line, you'll have to download the source code and the dependencies yourself.

1. Make sure you've got a working installation of Python 3. If you don't have Python on your device already, you can download the most recent version from [the official website](https://www.python.org/downloads/). If the installer gives you the option to add Python to your path, do so. If not, you'll have to set it manually (for Windows, [here](https://geek-university.com/python/add-python-to-the-windows-path/])'s a good tutorial.)

1. Make sure you've installed the Python library lxml (documentation is [here](https://lxml.de/installation.html)), which Heimdall uses to parse xml files. You can do so easily by running the following command:
``
pip install lxml
``

## How do I use it?
*These usage instructions only hold for the graphical user interface. If you're using the command line version of the tool, please read the usage instructions in our [Wiki](https://github.com/srbdts/heimdall/wiki/6.-Command-line-interface).*

### Input and output
#### Directories
###### Selecting directories
Click on the "Browse"-button next to "Input Directory" to select the input directory of your choice. Make sure the directory contains all and only the files that you want to process. It's currently not possible to process individual files (unless you're using the command line interface). If you wish to do so anyway, place the file in its own directory.

The same holds for the output directory: use the "Browse" button to select your preferred output directory. Make sure that the directory exists before you run the program (if you want the output to be written to a new directory, make one first), and bear in mind that previous output will be overwritten.

###### Sample input
You'll find three samples of compatible input formats in the *input* directory. One directory (*input/emma_sample*) contains some xml-files from the [EMMA corpus](https://www.uantwerpen.be/en/projects/mind-bending-grammars/emma-corpus/), another (*input/txt_sample*) contains a plain text file with sentences drawn from EMMA, and the third directory (*input/penn_preprocessed_sample*) contains three files from the [PPCEME](http://www.helsinki.fi/varieng/CoRD/corpora/PPCEME/) that have been made compatible with Heimdall (cf. the "format" paragraph below).

#### Format
Use the checkbox to indicate the format of your input files and, if it's xml, specify the "word" and "section" tags as well.

###### Input
Heimdall is compatible with all plain text files and most xml-files. Note that Xml-files are only processable if they have a dedicated tag to mark every word. In the following snippet, taken from the EMMA corpus, this tag is *&lt;w&gt;*. It does not matter if the tag has additional attributes or not - Heimdall will work as long as all relevant text in the file is immediately enclosed by a tag of the same kind.

```xml
<p>
    <w>My</w>
    <w>Lords</w>
    <w>,</w>
    <w>this</w>
    <w>was</w>
    <w>not</w>
    <w>all</w>
    <w>.</w>
</p>
```
In addition to the word-level tag, the xml-option requires you to specify a section-level tag. The section tag determines the size of the text blocks within which Heimdall looks for foreign language sequences. If your texts contain tags to mark single lines or paragraphs (like the *&lt;p&gt;*-tag in the snippet above), you could specify those, in which case Heimdall firsts extracts all *&lt;p&gt;*-elements, then collects all word-level elements within these paragraphs, and searches them for foreign language sequences.
 
###### Output
Regardless of the input format, Heimdall's main output will be a text file called *output.txt*, written to the output directory of your choice. The output file will contain the parameter settings of your run, as well as the actual output, structured as in the following snippet (from the EMMA sample). The tag combines three parts of information. It indicates (1) the detected language, (2) the order of the detected sequence in the file (i.e. "0" if its's the first foreign passage in the file, "1" if it's the second, etc.) , and (3) Heimdall's confidence about the tag. You can read more about the confidence score in our [Wiki](https://github.com/srbdts/heimdall/wiki/1.-How-does-it-work%3F).

FILENAME | TAG | SEQUENCE | SEQUENCE_LENGTH
---------|-----|----------|-----------------
A56130.xml |	latin/1/0.64286	| et genus et formam ( gold ) regina pecunia	| 9
A56130.xml | french/0/0.66406 |	par la grace de dieu , &c. au tres . e as barones de nostre eschequer . come entre autres choses que nous avoms grants al executors de testament margaret reigne dengleterre , les deniers grantez , que touts maners de dets que estoient duez de la dit reigne , de levant en la mesme manere come nos fesoms lever les nostres , sicome plus pleinement est contenus en lettres de nostre | 72

If your input files are xml, Heimdall offers you the additional option to tag them. If you tick the "tag files" box, the foreign word elements will receive a "lang" attribute whose value is set to the tag in the tables above. The tagged files will appear in the output directory, along with *output.txt*.

```xml
   <w>which</w>
   <w>recite</w>
   <w>;</w>
   <w>That</w>
   <w lang="latin/5/0.79592">aliae</w>
   <w lang="latin/5/0.79592">Reginae</w>
   <w lang="latin/5/0.79592">praedictum</w>
   <w lang="latin/5/0.79592">aurum</w>
   <w lang="latin/5/0.79592">illud</w>
   <w lang="latin/5/0.79592">recipere</w>
   <w lang="latin/5/0.79592">conſueverunt</w>
   <w lang="latin/5/0.79592">totis</w>
   <w lang="latin/5/0.79592">temporibus</w>
   <w lang="latin/5/0.79592">retroactis</w>
```

### Language settings
In the top right box, select the default language the text is written in. Check the languages you want to trace in the tickboxes below. There's no need to tick the box of the default language again - if the default language has been set correctly in the selection window on top, the language will be taken up in the analysis anyway.

### Parameter settings
In the right pane, you will find four sliders that allow you to adjust some of the properties of the taggers. The default values of the parameters are the ones that optimized Heimdall's [F1-score](https://en.wikipedia.org/wiki/F1_score) when tested on PPCEME and PPCBME. If you just want quick output, we'd recommend to leave them untouched. If, on the other hand, you want to tweak the precision/recall trade-off for your specific case study, feel free to play around with them. In that case, we kindly refer you to our [Wiki](https://github.com/srbdts/heimdall/wiki/4.-Parameter-Tweaking), where we explain what they mean and how they affect the tagging procedure.

### Run the program
If you've set all parameters, just press "GO!". If all goes as planned, the button will turn grey as long as Heimdall is processing your input. When it's finished, the button will turn blue again, you'll get a notification that your run was successful, and you can go and inspect your output in the output directory. If you get an error messsage (or nothing happens at all), please check the Troubleshooting section of our [Wiki](https://github.com/srbdts/heimdall/wiki/8.-Troubleshooting), or [let us know](https://www.uantwerpen.be/nl/personeel/sara-budts/) and we'll sort you out.

## Credits

Heimdall was developed by [Sara Budts](https://www.uantwerpen.be/nl/personeel/sara-budts/), for and in collaboration with the [Mind Bending Grammars team](https://www.uantwerpen.be/en/projects/mind-bending-grammars/) at the University of Antwerp. Don't hesitate to get in touch with us if you have any comments, questions, suggestions, or other kinds of feedback. The link attached to our names will lead you to our university website, where you'll find our contact details.
