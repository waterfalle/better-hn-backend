import pickle

'''
data_store.py

Explanation of initial_object:

"stories" (dictionary):
    - Is a dictionary of dictionaries which contains up to the top 500 stories on Hacker News.
    - The key is the id of the Hacker News `Item` (guaranteed to be unique integers).
    - The value is a dictionary, with all the properties of the Item
    - see more info on https://github.com/HackerNews/API

"ranked_order" (list of ints):
    - list of the item id's in `stories` in sorted order

"last_modified" (int):
    - Timestamp of the most recent time at which `stories` was modified.

'''

initial_object = {
    "stories":          {},
    "ranked_order":     [],
    "last_modified":    0
}

class Datastore:
    def __init__(self):
        self.store = initial_object
   
    def get(self):
        return self.store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.store = store
        with open('database.p', 'wb') as FILE:
            pickle.dump(self.store, FILE)

print('Loading Datastore...')

global data_store
data_store = Datastore()
