""" run_local_model.py: Deploys our local model to process GDELT data.

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

from local_model import generate_response, recommend_trade
from vector_database import retrieve_events_by_country, get_collection

import helpers


if __name__ == "__main__":

    # Get the collection of events from the vector database
    collection = get_collection(helpers.COLLECTION_NAME)

    #################################
    # TODO: Analyze model's summary of events in countries
    # Feel free to write your code here
    #################################
    country_of_interest = "United States"
    n_results = 10

    documents, _ = retrieve_events_by_country(
        collection, country_of_interest, n_results
    )

    prompt = "Hi There!"  # What should be the prompt?

    event_summary = generate_response(prompt)
    print(event_summary)

    #################################
    # TODO: Analyze the model's trade decisions
    # Feel free to write your code here
    #################################

    trade_decision = recommend_trade(country_of_interest, event_summary)
    print(trade_decision)
