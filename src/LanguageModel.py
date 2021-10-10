import os

class LanguageModel:
    def __init__(self,language,status,settings):
        self.normalize = settings["NORMALIZE"]
        self.language = language
        self.probsfile = os.path.join(settings["RESOURCEDIR"],language+".logprobs")
        self.status = status
        self.load()

    def load(self):
        """ load language model from log probability files """
        prob_data = open(self.probsfile,"r",encoding="utf-8")
        self.probs = {trigram.split("\t")[0]:float(trigram.split("\t")[2]) for trigram in prob_data.readlines()}

    def get_local_prob(self,trigram):
        """ return the probability of given trigram in current language """
        local_prob = 0
        if trigram in self.probs:
            return self.probs[trigram]
        else:
            return self.probs["UNKNOWN"]


