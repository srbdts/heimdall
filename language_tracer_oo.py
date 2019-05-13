from lxml import etree
import re, os, argparse
from config import *
from LanguageModel import *
from Tracer import *
from Word import *

def process_word_array(word_array,language_models,inputfile):
    tracers = [Tracer(lm.language) for lm in language_models if not lm.language == "english"]
    i = 0
    sequence_id = 0
    made_changes = False
    for word in word_array:
        if i < len(word_array)-1:
            word.pad(word_array[i+1].text)
        else:
            word.pad("THE_END")
        if not word.transparent:
            for lm in language_models:
                word.compute_probs(lm)
            word.set_flags(language_models)
        for tracer in tracers:
            tracer.update(word)
            if tracer.finished:
                tracer.finish(inputfile,outputfile,root)
                if tracer.finished:
                    made_changes = True
                tracer.initialize()
    for tracer in tracers:
        if not len(tracer.sequence) == 0:
            tracer.finish(inputfile,outputfile,root)
            if tracer.finished:
                made_changes = True
            tracer.initialize()
    return made_changes

def remove_previous_labels(previous_label,new_label):
    wrongly_labeled_ones = root.xpath("//w[@lang='"+previous_label+"']")
    print(" ".join([word.text for word in wrongly_labeled_ones]))
    for node in wrongly_labeled_ones:
        del node.attrib["lang"]
        if args.verbose:
            print("Removed label %s in favour of %s" % (previous_label,new_label))


def parse_input(parser):
    parser.add_argument("inputdir",help="The directory with the corpus files")
    parser.add_argument("outputdir",help="The directory to which the tagged files will be written.")
    parser.add_argument("-fn","--filename",required=False)
    parser.add_argument("-t","--tag",default=False,help="Tag the corpus files")
    parser.add_argument("-v","--verbose",default=False,help="Output progress information to the console")
    parser.add_argument("-sd","--statsdir",default=False,help="The directory to which the output file with the detected sequences will be written. If not specified, the files will be written to the output directory.")
    args = parser.parse_args()
    return args

parser = argparse.ArgumentParser(description="This script flags foreign language sequences in Early Modern English texts.")
args = parse_input(parser)
if args.statsdir:
    outputfile = open(os.path.join(args.statsdir,"output.txt"),"w")
else:
    outputfile = open(os.path.join(args.outputdir,"output.txt"),"w")

outputfile.write("**********************************************\n")
outputfile.write("PARAMETER SETTINGS:\n")
outputfile.write("Languages to identify: %s\n" % (LANGUAGES))
outputfile.write("Minimal confidence level: %s\n" % (MIN_CONFIDENCE))
outputfile.write("Maximum number of intervening words: %s\n" % (MAX_NOISE))
outputfile.write("Minimum sequence length: %s\n" % (MIN_SEQUENCE))
outputfile.write("Logprob threshold: %s\n" % (LOGPROB_THRESHOLD))
outputfile.write("**********************************************\n")

language_models = []
for language in LANGUAGES + ["english"]:
    language_models.append(LanguageModel(language))

if args.filename:
    inputfiles = [args.filename]
else:
    inputfiles = os.listdir(args.inputdir)

i=0
for inputfile in inputfiles:
    if args.verbose:
        if i%100 == 0:
            print("%s files processed. %s files to go..." % (i,len(inputfiles)-i))
    if os.path.isdir(os.path.join(args.inputdir,inputfile)):
        continue

    if INPUT_TYPE == "xml":
        root = etree.parse(os.path.join(args.inputdir,inputfile)).getroot()
        sections = root.findall(".//line")
    else:
        root = None
        sections = [line.strip() for line in open(os.path.join(args.inputdir,inputfile),"r").readlines()]
    #sections = [root]
    #print("Processing file %s - %s lines found." % (inputfile,len(sections)))
    total_changed = False
    for section in sections:
        if INPUT_TYPE == "xml":
            words = section.findall(".//w")
            word_array = [Word(word_node) for word_node in words if word_node.text]
        else:
            words = section.split(" ")
            word_array = [Word(word) for word in words]
        changed = process_word_array(word_array,language_models,inputfile)
        if changed:
            #print(words)
            total_changed = True
    i += 1
    if args.tag and total_changed:
        outputfile_xml = open(os.path.join(args.outputdir,inputfile.split("/")[-1]),"w")
        outputfile_xml.write(etree.tostring(root,pretty_print=True,encoding="unicode"))
        outputfile_xml.close()
        
outputfile.close()
if args.verbose:
    print("Finished.")

            






