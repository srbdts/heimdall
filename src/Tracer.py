#from config import TAG_MARKER, LANGUAGES, MIN_CONFIDENCE, MAX_NOISE, MIN_SEQUENCE, LOGPROB_THRESHOLD, INPUT_TYPE
from Word import *
from LanguageModel import *

class Tracer:
    def __init__(self,language,settings):
        self.language = language
        #index = settings["LANGUAGES"].index(language)
        self.min_confidence = settings["MIN_CONFIDENCE"]
        self.max_noise = settings["MAX_NOISE"]
        self.min_sequence = settings["MIN_SEQUENCE"]
        self.initialize()
        self.n_finished_sequences = 0
        self.input_type = settings["INPUT_TYPE"]

    def initialize(self):
        """ Initialize new tracer """
        self.n_words = 0 # transparent words not included
        self.total_conf = 0
        self.slipstream = 0
        self.changed = False
        self.sequence = []
        self.finished = False

    def update(self,word):
        """ Update tracer with a new word """
        
        # If the tracer isn't active yet
        if len(self.sequence) == 0:
            
            # And the word is transparant (i.e. punctuation): skip word
            if word.transparent:
                return
            
            # And the word is in the default language: skip word
            if word.probs[self.language] == 0:
                return
            
            # And the word is in the target language: start sequence
            else:
                self.sequence.append(word)
                self.n_words += 1
                self.total_conf += word.flags[self.language]
                return
            
        # If a sequence has been started
        else:
            
            # If the word is transparent: add to sequence without updating the stats
            if word.transparent:
                self.sequence.append(word)
                #Set the confidence to the current average confidence
                #word.flag[self.language] = self.total_conf/len(self.sequence)
                #self.total_conf += self.total_conf/len(self.sequence)
                return
            
            # Else, update (average) confidence of sequence with new word
            new_conf = word.flags[self.language]
            new_average_conf = (self.total_conf+new_conf)/(self.n_words+1)
            
            # If the word was not in the target language
            if word.flags[self.language] == 0:
                
                # but the confidence of the sequence is still sufficiently high:
                if new_average_conf >= 0.49:
                    # add word anyway if slipstream of non-target language words is not too long
                    if self.slipstream < self.max_noise:
                        self.sequence.append(word)
                        self.n_words += 1
                        self.total_conf += new_conf
                        self.slipstream += 1
                        return
                    # if slipstream is too long: finish sequence
                    else:
                        self.finished = True
                        return
                # if confidence is too low: finish sequence
                else:
                    self.finished = True
                    return
                
            # If the word was (potentially) in the target language: extend sequence
            else:
                self.sequence.append(word)
                self.n_words += 1
                self.total_conf += new_conf
                self.slipstream = 0
                return
    
    def finish(self,inputfile,outputfile,root):
        """ finish the completed sequence detected by the tracer """
        
        # Remove trailing words in non-target language
        i=0
        while i < self.slipstream:
            trailing_item = self.sequence.pop()
            if not trailing_item.transparent:
                self.n_words -= 1
                i += 1
        
        # Compute the confidence of the foreign sequence 
        sequence_conf = self.total_conf/self.n_words
        self.finished = False
        
        # If the sequence is long enough and the confidence is high enough
        if (self.n_words > self.min_sequence) and (sequence_conf > self.min_confidence):
            
            # Label sequence and write to output file (and tag input file if xml)
            self.finished = True
            value = str(round(sequence_conf,5))
            label = self.language+"/"+str(self.n_finished_sequences)+"/"+value
            outputfile.write("%s\t%s\t" % (inputfile,label))
            
            if self.input_type == "xml":
                plain_text_sequence = []
                for word in self.sequence:
                    if word.node.get("lang"):
                        previous_label = word.node.get("lang")
                        [previous_lang,previous_id,previous_conf] = previous_label.split("/")
                        if sequence_conf > float(previous_conf):
                            wrongly_labeled_ones = root.xpath("//w[@lang='"+previous_label+"']")
                            for node in wrongly_labeled_ones:
                                del node.attrib["lang"]
                            #remove_previous_labels(previous_label,label)
                            word.node.set("lang",label)
                    else:
                        word.node.set("lang",label)
                    plain_text_sequence.append(word.text)
            else:
                plain_text_sequence = [word.text for word in self.sequence]
            outputfile.write("%s\t%s\n" % (" ".join(plain_text_sequence),len(plain_text_sequence)))
            self.n_finished_sequences += 1

