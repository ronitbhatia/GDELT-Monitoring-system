""" vector_database.py: Contains functions for run_vector_database.py.

Copyright 2025, Cornell University

Cornell University asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including online repositories
such as Github.

Sharing solutions with current or future students of ENMGT5400 is
prohibited and subject to being investigated as a Code of Academic Integrity violation.

-----do not edit anything above this line---
"""

import chromadb
import chromadb.utils.embedding_functions as ef
import numpy as np
import os

import helpers


def create_database(
    client: chromadb.PersistentClient,
    collection_name: str,
    doc_ids: list[int],
    documents: list[str],
) -> chromadb.Collection:
    """Create a persistent vector database in a local folder, then create and populate a collection with documents.

    Args:
        client (chromadb.PersistentClient): The persistent client object.
        collection_name (str): The name of the collection.
        doc_ids (list[int]): The list of document ids.
        documents (list[str]): The list of documents.

    Returns:
        chromadb.Collection: The collection object.

    """

    collection = None
    embedding_function = ef.DefaultEmbeddingFunction()

    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################
    
    # Get or create the collection
    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=embedding_function
    )

    # Insert documents
    collection.add(ids=[str(doc_id) for doc_id in doc_ids], documents=documents)

    ##############################################################################

    return collection


def get_collection(collection_name: str) -> chromadb.Collection:
    """Get a collection from a persistent vector database.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        chromadb.Collection: The collection object.

    """
    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################
    client = chromadb.PersistentClient(path=helpers.DATABASE_FOLDER)
    embedding_function = ef.DefaultEmbeddingFunction()

    return client.get_collection(
        name=collection_name, embedding_function=embedding_function
    )
    ##############################################################################


def retrieve_events_by_country(
    collection: chromadb.Collection, country_of_interest: str, n_results: int
) -> tuple[list[str], np.array]:
    """Search for events that happened in a specific country.

    Args:
        collection (chromadb.Collection): The collection object.
        query_texts (list[str]): The list of query texts.
        n_results (int): The number of results to return.

    Returns:
        list[str]: The list of documents.
        np.array: The embeddings of the documents (n_results x embedding_size).

    """
    documents = []
    embeddings = np.array([])

    # The query text
    query = f"Happened at {country_of_interest}"

    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################

    # Perform query with embeddings included
    results = collection.query(
        query_texts=[query], n_results=n_results, include=["documents", "embeddings"]
    )

    # If no documents are retrieved, return empty results
    if not results["documents"]:
        return [], np.array([])

    # Flatten nested lists
    documents = [doc for sublist in results["documents"] for doc in sublist]
    embeddings = np.array(results["embeddings"]).squeeze(axis=0)  # Ensure correct shape

    # Apply filtering directly to documents and embeddings
    documents, embeddings = zip(*[
        (doc, emb) for doc, emb in zip(documents, embeddings) if country_of_interest in doc
        ]) if any(country_of_interest in doc for doc in documents) else ([], np.array([]))

    # Convert `zip` object back to lists for consistency
    documents, embeddings = list(documents), np.array(embeddings)
    ##############################################################################

    return documents, embeddings
