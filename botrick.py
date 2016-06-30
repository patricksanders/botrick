from pymongo import MongoClient
import random


class Markov(object):
        
    def __init__(self):
        self.collection = self.setup_db()

    def add_blob(self, text):
        tokens = text.lower().split()
        for i, t in enumerate(tokens):
            try:
                self.update_db(t, tokens[i+1])
            except IndexError:
                break

    def generate_text(self, length=20):
        result = []
        current = self.get_random_record()
        result.append(current['word'])
        for x in range(length):
            current = self.get_random_record(current)
            if current:
                result.append(current['word'])
            else:
                break

        return ' '.join(result)

    def get_random_record(self, seed=None):
        if not seed:
            count = self.collection.count()
            return self.collection.find()[random.randrange(count)]
        else:
            word = random.choice(seed['children'])
            return self.collection.find_one({'word': word})

    def get_record(self, word):
        return self.collection.find_one({'word': word})

    def setup_db(self):
        client = MongoClient()
        db = client.botrick
        return db.markov

    def update_db(self, base, new_word):
        self.collection.update_one({'word': base}, {'$push': {'children': new_word}}, upsert=True)

if __name__ == '__main__':
    markov = Markov()

    #with open('patrick.txt') as f:
    #    for line in f:
    #        markov.add_blob(line)

    print markov.generate_text(length=500)

