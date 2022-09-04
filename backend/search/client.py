from algoliasearch_django import algolia_engine

def get_client():
    return algolia_engine.client

def get_index(index_name='godman_Product'):
    client = get_client()
    index = client.init_index(index_name)
    return index

def perform_search(query, **kwargs):
    index = get_index() # initiate the index function
    print(kwargs)
    params = {}
    tags = ''
    if 'tags' in kwargs: # if tags in the kwargs
        tags = kwargs.pop('tags') or [] 
        # print(tags[0])
        if len(tags) != 0 and tags[0] != None: # the list tags is not empty and the tags are not None
            params['tagFilters'] = tags
    index_filters = [f"{k}: {v}" for k, v in kwargs.items() if v] # this will allow us be able to filter down based on
    # some added parameters like is public and users for more flexibility
    # NOTE: the 'if v' ending statement makes user the value is valid and not empty or none
    # print(index_filters)
    if len(index_filters) != 0: # checking if the index_filters is not empty
        params['facetFilters'] = index_filters # you add it to the facetFilters in the params 
    results = index.search(query, params)
    return results