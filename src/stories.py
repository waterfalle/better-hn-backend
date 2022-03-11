import asyncio
import httpx
from operator import itemgetter
from src.data_store import data_store

# CONSTANTS
HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
NO_ERROR = 200

def update_stories_v1():
    '''
    Updates the data_store["stories"] by using download_top_stories_v1()
    Sorts the new stories in descending order based on the story's score.

    Arguments:
        None

    Exceptions:
        None

    Return Value:
        None
    '''
    store = data_store.get()
    # get the top stories and their contents from Hacker News API
    top_stories = asyncio.run(download_top_stories_v1())

    # remove unecessary fields from each Item (descendants, kids etc)
    for story in top_stories:
        # specify "n/a" so that an exception is not raised if a key
        # doesn't exist
        story.pop("descendants", "n/a")
        story.pop("kids", "n/a")
        story.pop("type", "n/a")
        # don't need type as it will always be of type "story"

    # sort in descending order based on the story's score
    top_stories.sort(key=itemgetter("score"), reverse=True)
    # replace the old copy with the new copy
    store["stories"] = top_stories
    data_store.set(store)

async def download_top_stories_v1():
    '''
    Asynchronously gets the content of the top 500 Hacker News `Item`s.
    This is much faster than using requests synchronously:
        - requests (sync): ~6 minutes
        - async: ~6 seconds
    
    Arguments:
        None
        
    Exceptions:
        None

    Return Value:
        top_stories (list of dictionaries):
            - contains a dictionary for each Hacker News Item.
    '''
    tasks = []
    async with httpx.AsyncClient() as session:
        top_story_list = await session.get(HN_TOP_STORIES_URL)
        assert (top_story_list.status_code == NO_ERROR)
        top_story_list = top_story_list.json()

        for story_id in top_story_list:
            tasks.append(
                asyncio.create_task(session.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"))
            )
        
        top_stories = await asyncio.gather(*tasks)
        top_stories = [x.json() for x in top_stories if x.status_code == NO_ERROR]

        return top_stories

def get_stories_v1(num_stories):
    '''
    Returns the specified `num_stories` number of top stories.

    Arguments:
        num_stories (int): number of stories to return
        
    Exceptions:
        None

    Return Value:
        - stories:
            list containing dicitionaries of the Items.
    '''
    store = data_store.get()
    stories = store["stories"]
    # check that num_stories is valid
    assert (1 <= num_stories <= 500)
    # return the specified number of stories
    return {
        "stories":  stories[:num_stories]
    }
