import spacy
import pickle
from spacy.tokens import DocBin

nlp = spacy.blank("en")
# Load Data
training_data = pickle.load(open('../data/pickle/TrainData.pickle','rb'))
testing_data = pickle.load(open('../data/pickle/TestData.pickle','rb'))

# the DocBin will store the example documents
db_train = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations['entities']:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db_train.add(doc)
db_train.to_disk("../data/spacy/train.spacy")

# the DocBin will store the example documents
db_test = DocBin()
for text, annotations in testing_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations['entities']:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db_test.add(doc)
db_test.to_disk("../data/spacy/test.spacy")
