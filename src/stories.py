from src.data_store import data_store
import requests
import copy
from operator import itemgetter
from threading import Thread

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/2921983.json?print=pretty"
NO_ERROR = 200

# TODO: need to add threading for performance when downloading
def update_stories_v1():
    store = data_store.get()
    # we are making a separate copy of stories, as this way we can make changes
    # in the background while allowing users to still access the stored copy
    # This may result in a slight delay however, between the available stories
    # and the current top stories
    stories = copy.deepcopy(store["stories"])
    
    # retrieve the list of top 500 story id's from Hacker News
    resp = requests.get(HN_TOP_STORIES_URL)
    assert (resp.status_code == NO_ERROR)
    top_stories = resp.json()

    threads = []

    for story_id in top_stories:
        if story_id not in stories.keys():
            threads.append(Thread(target=add_story, args=(story_id, stories)))
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    remove_stories(top_stories, stories)

    ranked_order = sorted(stories.values(), key=itemgetter("score"))

    # replace the old copy with the new copy
    store["stories"] = stories
    store["ranked_order"] = ranked_order
    data_store.set(store)
    return


def add_story(story_id, stories):
    '''
    Adds a new story into the datastore's stories.

    Arguments:
        story_id    (int) : unique id of the Hacker News "Item"
        stories     (dict): currently stored stories
        
    Exceptions:
        None

    Return Value:
        None
    '''
    resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
    assert (resp.status_code == NO_ERROR)
    new_story = resp.json()
    stories[story_id] = new_story
    return

def remove_stories(top_stories, stories):
    '''
    Removes the stored stories which are no longer in the top 500.

    Arguments:
        top_stories (list): list of the new top 500 stories
        stories     (dict): currently stored stories
        
    Exceptions:
        None

    Return Value:
        None
    '''
    # this returns a set of the stores stories which are no longer in the 
    # top 500
    remove = set(stories.keys()).difference(set(top_stories))
    for i in remove:
        stories.pop(i)
    return

def get_stories_v1(num_stories):
    store = data_store.get()
    stories = store["stories"]
    ranked_order = store["ranked_order"]
    
    return stories

    print(stories, ranked_order)

    data = {}
    # stories to return
    for i in range(num_stories):
        data[ranked_order[i]] = stories[ranked_order[i]]
    return stories