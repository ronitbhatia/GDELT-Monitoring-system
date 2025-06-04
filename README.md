# GDELT-Monitoring-system

## Overview

This project simulates the role of a portfolio manager at a Global Macro Hedge Fund by using a **local Large Language Model (LLM)** to monitor global news events and generate **long/short investment recommendations** at the **country level**.

Leveraging real-world data from [GDELT](https://www.gdeltproject.org/), the project involves scraping, processing, and analyzing global event data, storing it in a **vector database**, and using **LLM reasoning** for financial decision-making — **completely locally**.

## Setup Instructions

### Environment Setup

Use a virtual environment to manage dependencies:

```bash
conda create --name enmgt5400p2 python=3.12
conda activate enmgt5400p2
pip install -r requirements.txt
```

### Install Local LLM

Install [Ollama](https://ollama.com/) and pull the LLaMA 3.2B model:

```bash
ollama pull llama3.2:3b
```

Ensure Ollama is running the model before invoking LLM features.

## Project Structure

```
.
├── download_data.py        # Webscraping GDELT file URLs
├── transform_data.py       # Parse event data and clean for database
├── vector_database.py      # Store and retrieve from Chroma DB
├── run_vector_database.py  # EDA, embedding visualization, vector tests
├── local_model.py          # Local LLM interaction and trade logic
├── run_local_model.py      # End-to-end system execution
├── test_*.py               # Unit tests for all modules
├── data/                   # Contains provided .CSV event files
└── requirements.txt        # Required Python packages
```

## Features

### 1. Webscraping (GDELT)

* Extract file names and URLs from the GDELT website.
* Download raw event files.

### 2. Data Transformation

* Extract meaningful text summaries from URLs.
* Clean and filter event datasets.
* Focus on selected columns only.

### 3. Vector Database

* Use [Chroma](https://www.trychroma.com/) for text embedding and retrieval.
* Query similar events by country.
* Visualize embeddings with PCA and t-SNE.

### 4. Local Language Model

* Summarize country-specific events.
* Recommend long/short positions.
* Leverage prompt engineering to optimize outputs.

## Running Tests

Run all tests to validate your implementation:

```bash
python -m unittest discover
```

## Report Expectations

The final report (max 10 pages) must include:

* EDA on GDELT events
* Database structure & vectorization critique
* Embedding visualization discussion
* Prompt design justification
* Evaluation methodology for LLM + portfolio system

See `report_template.docx` or `report_template.tex` on Canvas.

## Notes

* Only local models (no API calls) are allowed.
* Ethical and legal concerns around webscraping must be addressed.
* All `.py` files contain `TODO` sections for you to implement.
* Appendices and references don’t count toward the page limit.

## References

* [GDELT Project](https://www.gdeltproject.org/)
* [Chroma Documentation](https://docs.trychroma.com/docs/overview/getting-started)
* [Ollama](https://ollama.com/)
* [Prompting Strategies - Google AI](https://ai.google.dev/gemini-api/docs/prompting-strategies)

---

Let me know if you'd like this converted into another format (like PDF or DOCX).
