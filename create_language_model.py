import os, argparse, math, re
from lxml import etree


def get_words(f,tag):
    padded_words = []
    if tag:
        root = etree.parse(f).getroot()
        words = root.findall(".//" + tag)
        words = [w for w in words if w.text]
        if len(words) == 0:
            return []
        padded_words = []
        for i in range(len(words)-1):
            word = words[i].text
            word = word.replace("ſ","s")
            if re.match(r'[?.!;, 0123456789\W]+',word,flags=re.UNICODE):
                continue
            next_word = words[i+1].text
            if re.match(r'[?.!;, ]+',next_word,flags=re.UNICODE):
                padded_words.append(" " + word.lower() + next_word.lower() + " ")
            else:
                padded_words.append(" " + word.lower() + " ")
        return padded_words
    else:
        lines = open(f,"r").readlines()
        for line in lines:
            words = line.lower().replace("ſ","s").strip().split(" ")
            padded_words.extend([" "+word+" " for word in words])
        return padded_words




p = argparse.ArgumentParser()
p.add_argument("inputdir")
p.add_argument("outputfile")
p.add_argument("--tag",dest="tag",default=None)
args = p.parse_args()

trigramdic = {}

total_trigrams = 0
for file in os.listdir(args.inputdir):
    file = os.path.join(args.inputdir,file)
    words = get_words(file,args.tag)
    for word in words:
        for i in range(len(word)-3):
            total_trigrams += 1
            trigram = word[i:i+3]
            if not trigram in trigramdic:
                trigramdic[trigram] = 1
            else:
                trigramdic[trigram] += 1

opf = open(args.outputfile,"w")
for trigram,count in trigramdic.items():
    opf.write("%s\t%s\t%s\n" % (trigram,count,math.log10(count/total_trigrams)))

opf.close()
