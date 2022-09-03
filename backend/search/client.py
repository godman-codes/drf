from algoliasearch_django import algolia_engine

def get_client():
    return algolia_engine.client

def get_index(index_name='godman_Product'):
    client = get_client()
    index = client.init_index(index_name)
    return index

def perform_search(query, **kwargs):
    index = get_index() # initiate the index function
    params = {}
    tags = ''
    if 'tags' in kwargs: # if tags in the kwargs
        tags = kwargs.pop('tags') or [] 
        if len(tags) != 0: # the list tags is not empty
            params['tagFilters'] = tags
    results = index.search(query, params)
    return results