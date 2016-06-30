from pymongo import MongoClient
import random


class Markov(object):
    def __init__(self):
        self.collection = self.setup_db()

    def add_blob(self, text):
        """
        Add a blob of text to the markov corpus database.

        :param text: string
        """
        tokens = text.lower().split()
        for i, t in enumerate(tokens):
            try:
                self.update_db(t, tokens[i + 1])
            except IndexError:
                break

    def generate_text(self, length=20):
        """
        Generate a snippet of text with a maximum of `length` words.

        :param length: int
        :return: string
        """
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
        """
        Retrieve a random entry from markov collection.

        :param seed: pymongo markov document
        :return: pymongo markov document
        """
        if not seed:
            count = self.collection.count()
            return self.collection.find()[random.randrange(count)]
        else:
            word = random.choice(seed['children'])
            return self.collection.find_one({'word': word})

    def get_record(self, word):
        """
        Retrieve word record from markov collection.
        :param word: string
        :return: pymongo markov document
        """
        return self.collection.find_one({'word': word})

    def setup_db(self):
        """
        Set up database connection.
        :return: pymongo collection
        """
        client = MongoClient()
        db = client.botrick
        return db.markov

    def update_db(self, word, new_child):
        """
        Add words to markov collection using `upsert` methodology.
        :param word: string
        :param new_child: string
        """
        self.collection.update_one({'word': word}, {'$push': {'children': new_child}}, upsert=True)

