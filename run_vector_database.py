""" run_vector_database.py: Creates a vector database to store GDELT data and retrieves events by country.
This script also visualizes the clusters of events using t-SNE and PCA.

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

import os
import time

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import chromadb
import numpy as np

import helpers
from transform_data import read_gdelt
from vector_database import create_database, retrieve_events_by_country, get_collection


if __name__ == "__main__":

    # Initialize a persistent client
    os.makedirs(helpers.DATABASE_FOLDER, exist_ok=True)
    client = chromadb.PersistentClient(
        path=helpers.DATABASE_FOLDER,
    )

    #################################
    # Create a vector collection. This can be a bit slow...
    # depending on your hardware and patience.
    # If you have already created the collection, set create_database_from_files to False.
    #################################

    #Define files and locate data folder
    files = ["20250212.export.CSV", "20250213.export.CSV"]
    data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

    #Create vector database (if needed)
    create_database_from_files = True

    for file in files:
        file_path = os.path.join(data_folder, file)

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"⚠️ Skipping {file} (File Not Found)")
            continue

        # Read dataset
        df = read_gdelt(data_folder=data_folder, filename=file)
        if df.empty:
            print(f"Skipping {file} (Empty File)")
            continue

        # Convert data into required format
        documents = [
            f"Event: {x}. Impact location: {y}. Goldstein scale: {z}."
            for x, y, z in zip(df.Text, df.ActionGeo_FullName, df.GoldsteinScale)
        ]

        # Start time tracking
        start_time = time.time()

        if create_database_from_files:
            collection = create_database(
                client=client,
                collection_name=helpers.COLLECTION_NAME,
                doc_ids=df.index.tolist(),
                documents=documents,
            )
        else:
            collection.add(
                documents=documents,
                ids=df.index.tolist()
            )

        print(f"{file} -- Time taken to load data: {time.time() - start_time:.2f} seconds.")
        create_database_from_files = False  # Ensure database creation runs only once


    #################################
    #  TODO: Perform exploratory data analysis on the dataframes/collections
    #################################

    #Exploratory Data Analysis (EDA)
    print("\nExploratory Data Analysis (EDA):")
    df_sample = read_gdelt(data_folder, files[0])

    if not df_sample.empty:
        print(df_sample.head())

        #Country Distribution
        top_countries = df_sample["ActionGeo_FullName"].value_counts().head(10)
        plt.figure(figsize=(10, 5))
        sns.barplot(x=top_countries.index, y=top_countries.values)
        plt.xticks(rotation=45)
        plt.title("Top 10 Countries with Most Events")
        plt.xlabel("Country")
        plt.ylabel("Event Count")
        plt.show()
    else:
        print("No data available for EDA.")

    #################################
    #  TODO: Try querying the database for events in different countries
    #################################

    country_of_interest = "United States"
    n_results = 5

    try:
        collection = client.get_collection(helpers.COLLECTION_NAME)
        documents, embeddings = retrieve_events_by_country(collection, country_of_interest, n_results)
        print("\nRetrieved Events:\n", documents)
    except Exception as e:
        print(f"Error retrieving events: {e}")
        documents, embeddings = [], None

    #################################
    # TODO: Plot clusters using t-SNE
    # You probably need to import libraries in requirements.txt
    #################################

    # Apply t-SNE for dimensionality reduction
    if embeddings is not None and len(embeddings) > 1:
        try:
            # Perform t-SNE
            tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(embeddings) - 1))
            tsne_results = tsne.fit_transform(embeddings)

            # Plot t-SNE results
            plt.figure(figsize=(8, 6))
            plt.scatter(tsne_results[:, 0], tsne_results[:, 1], alpha=0.7)
            plt.title(f"t-SNE Visualization of Events in {country_of_interest}")
            plt.xlabel("t-SNE Component 1")
            plt.ylabel("t-SNE Component 2")
            plt.show()
        except Exception as e:
            print(f"Error in t-SNE visualization: {e}")

    #################################
    # TODO: Plot clusters using PCA
    # You probably need to import libraries in requirements.txt
    #################################

    # Convert embeddings to NumPy array if not already
        try:
            # Perform PCA
            pca = PCA(n_components=2)
            pca_results = pca.fit_transform(embeddings)

            # Plot PCA results
            plt.figure(figsize=(8, 6))
            plt.scatter(pca_results[:, 0], pca_results[:, 1], alpha=0.7)
            plt.title(f"PCA Visualization of Events in {country_of_interest}")
            plt.xlabel("Principal Component 1")
            plt.ylabel("Principal Component 2")
            plt.show()
        except Exception as e:
            print(f"Error in PCA visualization: {e}")
    else:
        print("Not enough embeddings for visualization.")