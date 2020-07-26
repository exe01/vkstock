from djantimat.helpers import PymorphyProc


class PartialCensor(PymorphyProc):
    @staticmethod
    def censor(text, repl='*'):
        for word in PymorphyProc._gen(text):
            censor_part = repl*(len(word) - 2)
            replace_word = word[0] + censor_part + word[-1]
            text = text.replace(word, replace_word)
        return text
