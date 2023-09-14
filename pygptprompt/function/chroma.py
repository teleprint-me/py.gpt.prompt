"""
pygptprompt/function/chroma.py
"""


def query_chroma_collection(collection, query_text, metadata_filter=None):
    """
    Query a Chroma collection and return the results.

    This function queries a given Chroma collection based on the provided
    query text and optional metadata filter. It returns up to 10 results
    that match the query.

    Parameters:
        collection (object): The Chroma collection to query.
        query_text (str): The text to use for querying the collection.
        metadata_filter (dict, optional): A dictionary containing metadata filters. Defaults to None.

    Returns:
        object: The query result containing matched documents and metadata.
    """
    query_result = collection.query(
        query_texts=[query_text],
        n_results=10,
        where=metadata_filter,
    )
    return query_result
