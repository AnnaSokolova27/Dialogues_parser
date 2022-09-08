import csv
import spacy
from natasha import MorphVocab, NamesExtractor

nlp = spacy.load("ru_core_news_lg")
morph_vocab = MorphVocab()
extractor = NamesExtractor(morph_vocab)

greetings = ['добрый день', 'здравствуйте', 'добрый вечер', 'доброе утро']
farewells = ['до свидания', 'всего хорошего', 'всего доброго']
names = ['зовут', 'это']
companies = ['компания', 'компании', 'компанию']
greetingM = False
farewellM = False
dialogue = '0'
newRow = []
text = ''
all=[]

def goodManagerCheck(newRow, greetingM, farewellM, dialogue):
    if (greetingM == True and farewellM == True):
        newRow.append(dialogue)
        for i in range(0, 3):
            newRow.append('-')
        newRow.append('goodManager = True')
    else:
        newRow.append(dialogue)
        for i in range(0, 3):
            newRow.append('-')
        newRow.append('goodManager = False')
    return newRow

with open("test_data.csv", 'r+', encoding='utf-8') as file:
    with open("test_data.csv", 'r+', encoding='utf-8') as fileout:
        file_reader = csv.reader(file, delimiter = ",")
        file_writer = csv.writer(fileout, delimiter = ",")
        row = next(file_reader)
        row.append('insight')
        all.append(row)
        for row in file_reader:
            if (row[0] != dialogue and row[0] != 'dlg_id'):
                newRow = goodManagerCheck(newRow,  greetingM, farewellM, dialogue)
                all.append(newRow)
                newRow = []
                greetingM = False
                farewellM = False
                companyName = ''
                dialogue = int(dialogue)
                dialogue = dialogue + 1
                dialogue = str(dialogue)
            if(row[2] == 'manager'):
                row[3] = row[3].lower()
                for greeting in greetings:
                    if greeting in row[3]:
                        greetingM = True
                        text = text + 'greetingPhrase = ' + greeting + ' '
                for farewell in farewells:
                    if farewell in row[3]:
                        farewellM = True
                        text = text + 'farewellPhrase = ' + farewell + ' '
                for company in companies:
                    if company in row[3]:
                        doc = nlp(row[3])
                        for word in doc:
                            if (str(word.head) == company and word.dep_ == 'appos'):
                                text = text + 'companyName = ' + word.text + ' '
                matches = extractor(row[3])
                for match in matches:
                    if (match.fact.first is not None):
                        for name in names:
                            if name in row[3][match.start-6:match.stop+6]:
                                text = text + 'nameManager = ' + row[3][match.start:match.stop] + ' '
            row.append(text)
            text = ''
            all.append(row)
        newRow = goodManagerCheck(newRow,  greetingM, farewellM, dialogue)
        all.append(newRow)
        file_writer.writerows(all)