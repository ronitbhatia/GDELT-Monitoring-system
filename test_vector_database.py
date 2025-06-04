""" test_vector_database.py

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

import unittest
import chromadb
import numpy as np
import os

from vector_database import create_database, retrieve_events_by_country

# Define a temporary directory for testing
TEST_DATABASE_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_db_delete_me"
)


class TestVectorDatabase(unittest.TestCase):

    def setUp(self):
        # Create the test database folder
        os.makedirs(TEST_DATABASE_FOLDER, exist_ok=True)
        # Clean up any existing collections before each test
        self.client = chromadb.PersistentClient(
            path=TEST_DATABASE_FOLDER,
            settings=chromadb.config.Settings(allow_reset=True),
        )

    def tearDown(self):
        # Reset the client to clean up the database
        self.client.reset()

    def test_create_database(self):
        collection_name = "test_collection"
        doc_ids = ["1", "2", "3"]
        documents = ["Document 1", "Document 2", "Document 3"]

        collection = create_database(self.client, collection_name, doc_ids, documents)
        self.assertIsInstance(collection, chromadb.Collection)
        # There should be 3 documents in the collection
        self.assertEqual(collection.count(), 3)

    def test_retrieve_events_by_country(self):
        filepath = TEST_DATABASE_FOLDER
        collection_name = "test_collection_country"
        doc_ids = ["1", "2", "3", "4"]
        documents = [
            "Event 1 happened at France",
            "Event 2 happened at Germany",
            "Event 3 happened at France",
            "Event 4 happened at France",
        ]
        collection = create_database(self.client, collection_name, doc_ids, documents)

        # ============= Germany
        country_of_interest = "Germany"
        n_results = 1

        retrieved_docs, retrieved_embeddings = retrieve_events_by_country(
            collection, country_of_interest, n_results
        )

        # The function should return the correct number of results
        self.assertIsInstance(retrieved_embeddings, np.ndarray)
        self.assertEqual(len(retrieved_docs), n_results)
        self.assertEqual(retrieved_embeddings.shape[0], n_results)

        # Check if the country of interest is in the retrieved documents
        self.assertIn("Germany", retrieved_docs[0] or retrieved_docs[1])

        # ============ France
        country_of_interest = "France"
        # If requested number of results is more than the actual results,
        # the function should return all available results
        n_results = 5
        retrieved_docs, retrieved_embeddings = retrieve_events_by_country(
            collection, country_of_interest, n_results
        )
        self.assertEqual(len(retrieved_docs), 3)
        self.assertEqual(retrieved_embeddings.shape[0], 3)


if __name__ == "__main__":
    unittest.main()
