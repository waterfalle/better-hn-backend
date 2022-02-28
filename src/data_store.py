'''
data_store.py

Explanation of initial_object:

"stories" (list):
    - Is a list of dictionaries which contains up to the top 500 stories on Hacker News.
    - items in stories are sorted in descending order based on the item's score.
    - see more info on https://github.com/HackerNews/API
'''

initial_object = {
    "stories":  []
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

print('Loading Datastore 😁 ...')

global data_store
data_store = Datastore()
