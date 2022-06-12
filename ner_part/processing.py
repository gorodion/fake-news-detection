from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("russian")


def stemming(text:str)->str:
    text = text.split(' ')
    return ' '.join(stemmer.stem(t) for t in text)

