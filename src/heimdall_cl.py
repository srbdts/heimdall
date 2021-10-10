from lxml import etree
import re, os, argparse
from config import *
from LanguageModel import *
from Tracer import *
from Word import *

def process_word_array(word_array,language_models,inputfile,outputfile,root,settings):
    """ Detect foreign sequences in provided word array """
    # Create a tracer for all languages you want to detect
    tracers = [Tracer(lm.language,settings) for lm in language_models if not lm.status == "default"]
    
    # For each word in the current section:
    i = 0
    sequence_id = 0
    made_changes = False
    for word in word_array:
        
        # Pad the word with its neighbours to get the trigrams at the edges right
        if i < len(word_array)-1:
            word.pad(word_array[i+1].text)
        else:
            word.pad("THE_END")
            
        # Skip transparent words (e.g. punctuation)
        # Compute the probability of the word in each language and flag it accordingly
        if not word.transparent:
            for lm in language_models:
                word.compute_probs(lm)
            word.set_flags(language_models)
            
        # Append the word to each tracer    
        for tracer in tracers:
            tracer.update(word)
            
            # If the end of a foreign sequence has been reached:
            if tracer.finished:
                # Finalize the sequence
                tracer.finish(inputfile,outputfile,root)
                if tracer.finished:
                    made_changes = True
                # Re-initialize the tracer
                tracer.initialize()
    
    # Finalize all non-finalized sequences when the end of the word array has been reached
    for tracer in tracers:
        if not len(tracer.sequence) == 0:
            tracer.finish(inputfile,outputfile,root)
            if tracer.finished:
                made_changes = True
            tracer.initialize()
            
    # Return True if foreign sequences have been found; False if not
    return made_changes

def remove_previous_labels(previous_label,new_label):
    """ Overwrite old labels with new ones in case of conflicts """
    wrongly_labeled_ones = root.xpath("//w[@lang='"+previous_label+"']")
    print(" ".join([word.text for word in wrongly_labeled_ones]))
    for node in wrongly_labeled_ones:
        del node.attrib["lang"]
        if args.verbose:
            print("Removed label %s in favour of %s" % (previous_label,new_label))

def load_settings_from_config(args):
    """ Load settings from configuration file """
    if args.tag:
        tag_files = True
    else:
        tag_files = False
    settings = {
        "TAG_FILES": tag_files,
        "INPUTDIR": args.inputdir,
        "OUTPUTDIR": args.outputdir,
        "RESOURCEDIR": RESOURCEDIR,
        "INPUT_TYPE": INPUT_TYPE,
        "WORD_MARKER": WORD_MARKER,
        "SECTION_MARKER": SECTION_MARKER,
        "DEFAULT_LANGUAGE": DEFAULT_LANGUAGE,
        "LANGUAGES": LANGUAGES,
        "MIN_CONFIDENCE": MIN_CONFIDENCE,
        "MAX_NOISE": MAX_NOISE,
        "MIN_SEQUENCE": MIN_SEQUENCE,
        "LOGPROB_THRESHOLD": LOGPROB_THRESHOLD,
        "NORMALIZE": NORMALIZE,
    } 
    return settings

def parse_input(parser):
    """ Parse command line arguments """
    parser.add_argument("inputdir",help="The directory with the corpus files")
    parser.add_argument("outputdir",help="The directory to which the tagged files will be written.")
    parser.add_argument("-fn","--filename",required=False)
    parser.add_argument("-t","--tag",default=False,help="Tag the corpus files")
    parser.add_argument("-v","--verbose",default=False,help="Output progress information to the console")
    args = parser.parse_args()
    return args

def trace(settings=None):
    """ Main function """
    if not settings:
        parser = argparse.ArgumentParser(description="This script flags foreign language sequences in Early Modern English texts.")
        args = parse_input(parser)
        settings = load_settings_from_config(args)
    else:
        args = None

    outputfile = open(os.path.join(settings["OUTPUTDIR"],"output.txt"),"w",encoding="utf-8")

    outputfile.write("**********************************************\n")
    outputfile.write("*** PARAMETER SETTINGS:\n")
    outputfile.write("*** Inputdir: %s\n" % (settings["INPUTDIR"]))
    outputfile.write("*** Outputdir: %s\n" % (settings["OUTPUTDIR"]))
    outputfile.write("*** Resourcedir: %s\n" % (settings["RESOURCEDIR"]))
    outputfile.write("*** Word marker: %s\n" % (settings["WORD_MARKER"]))
    outputfile.write("*** Section marker: %s\n" % (settings["SECTION_MARKER"]))
    outputfile.write("*** Default language: %s\n" % settings["DEFAULT_LANGUAGE"])
    outputfile.write("*** Languages to identify: %s\n" % (settings["LANGUAGES"]))
    outputfile.write("*** Minimal confidence level: %s\n" % (settings["MIN_CONFIDENCE"]))
    outputfile.write("*** Maximum number of intervening words: %s\n" % (settings["MAX_NOISE"]))
    outputfile.write("*** Minimum sequence length: %s\n" % (settings["MIN_SEQUENCE"]))
    outputfile.write("*** Logprob threshold: %s\n" % (settings["LOGPROB_THRESHOLD"]))
    outputfile.write("*** Normalize: %s\n" % (settings["NORMALIZE"]))
    outputfile.write("**********************************************\n")

    # Load language models
    language_models = []
    for language in settings["LANGUAGES"]:
        language_models.append(LanguageModel(language,"trace",settings))
    language_models.append(LanguageModel(settings["DEFAULT_LANGUAGE"],"default",settings))

    # Load input files
    if args and args.filename:
        inputfiles = [args.filename]
    else:
        inputfiles = os.listdir(settings["INPUTDIR"])
    print(inputfiles)
    
    # Process each file
    i=0
    for inputfile in inputfiles:
        
        # Report progress in verbose mode
        if args and args.verbose:
            if i%100 == 0:
                print("%s files processed. %s files to go..." % (i,len(inputfiles)-i))
                
        # Skip directories
        if os.path.isdir(os.path.join(settings["INPUTDIR"],inputfile)):
            continue

        # Collect all text sections
        if settings["INPUT_TYPE"] == "xml":
            root = etree.parse(os.path.join(settings["INPUTDIR"],inputfile)).getroot()
            sections = root.findall(".//"+settings["SECTION_MARKER"])
        else:
            root = None
            sections = [line.strip() for line in open(os.path.join(settings["INPUTDIR"],inputfile),"r").readlines()]
        #sections = [root]
        #print("Processing file %s - %s lines found." % (inputfile,len(sections)))
        
        # Process each section
        total_changed = False
        for section in sections:
            
            # Collect all words in the section
            if settings["INPUT_TYPE"] == "xml":
                words = section.findall(".//"+settings["WORD_MARKER"])
                word_array = [Word(word_node,settings) for word_node in words if word_node.text]
            else:
                words = section.split(" ")
                word_array = [Word(word,settings) for word in words]
                
            # Process words and keep track of any changes
            changed = process_word_array(word_array,language_models,inputfile,outputfile,root,settings)
            if changed:
                #print(words)
                total_changed = True
        
        # Tag inputfile with all detected sequences
        i += 1
        if settings["TAG_FILES"] and settings["INPUT_TYPE"] == "xml":
            outputfile_xml = open(os.path.join(settings["OUTPUTDIR"],inputfile.split("/")[-1]),"w",encoding="utf-8")
            outputfile_xml.write(etree.tostring(root,pretty_print=True,encoding="unicode"))
            outputfile_xml.close()
            
    outputfile.close()
    if args and args.verbose:
        print("Finished.")

if __name__ == "__main__":
    trace()

            






