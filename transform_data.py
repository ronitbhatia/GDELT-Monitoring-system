"""transform_data.py: Contains functions for run_vector_database.py.

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
import re
import pandas as pd
from helpers import GDELTFIELDNAMES


def parse_url(url: str) -> str:
    """URLs may contain information on what the webpage is about. This function
    parses a URL to extract the "title" of a webpage, which is returned as a string.
    We will use this function to parse URLs from the GDELT database.

    Args:
        url (str): a URL

    Returns:
        str: the title of the webpage

    Note the following requirements:

    - A URL is contains segments separated by "/". The segment of interest in the one with
    3 or more dashes ("-") in the text as that is likely to contain the title of the webpage.
    For brevity, we will refer to this segment as "the segment".

    - If there are multiple segments with more than three dashes, "the segment" is furthest segment
    from the root of the URL. For example, in the URL "https://{1}/{2}/{3}/{4}", the furthest segment is "4".

    - If there are no segments with at least three dashes, return None.

    - The segment must have fewer than 8 digits (< 8).

    - Dashes in the segment are replaced with spaces.

    - "Words" in the segment with six or more digits are removed.
       Example:
       "A999999" is removed.
       "A99999" is kept.

    - Words in the segment are separated by a single space.

    - Replace ".cms" and ".html" in the string to ""

    - The return string is in lowercase.

    - The return string does not contain the following characters at the beginning or end of the string:
      " ", "/", ".". In other words, there are no leading or trailing spaces, slashes, or full stops

    - In an edge case where the segment is an empty string, return None.


    Here are some examples:

    1. https://www.yahoo.com/news/russian-military-convoy-blocked-entering.html
    -> return "russian military convoy blocked entering"

    2. https://www.yahoo.com/news/russian-military-convoy-blocked-entering-12345678.html
    -> return None because the segment contains 8 or more digits

    3. https://www.den-ver-post.com/2025/02/11/king-soopers-union-strike-lawsuit-restraining-order-A999999/
    -> return "king soopers union strike lawsuit restraining order"

    4. https://www.yahoo.com/news/russian---military--convoy-blocked-entering.html
    -> return "russian military convoy blocked entering"

    """

    page_title = None

    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################


    if not isinstance(url, str) or not url.startswith("http"):
        return None  # Handle invalid URLs

    # Normalize and extract segments
    url = url.strip("/")
    segments = url.split("/")

    # Identify all valid segments: must contain at least 3 dashes ("-")
    valid_segments = [segment for segment in segments if segment.count("-") >= 3]
    
    while valid_segments:
        segment = valid_segments.pop()  # Start with the furthest valid segment
        
        # Remove file extensions (.cms, .html)
        segment = re.sub(r"\.cms|\.html$", "", segment)

        # Count total number of digits in the segment
        total_digits = sum(c.isdigit() for c in segment)

        # If the segment contains 8 or more digits in total, continue to the next farthest valid segment
        if total_digits >= 8:
            continue

        # Replace multiple dashes with a single space
        segment = re.sub(r"-+", " ", segment)

        # Remove words where total digits in the word are 6 or more
        words = segment.split()
        filtered_words = [word for word in words if sum(c.isdigit() for c in word) < 6]

        # If the resulting segment is empty, continue to the next farthest valid segment
        if not filtered_words:
            continue

        # Join the words into the final title
        title = " ".join(filtered_words).strip(" /.")

        return title.lower() if title else None
    
    return None

    ##############################################################################
    return page_title


def read_gdelt(data_folder: str, filename: str) -> pd.DataFrame:
    """
    Given a raw CSV file, create a dataframe with the following characteristics:

    1. Set GLOBALEVENTID (str) as the index of the dataframe.

    2. Contains the following columns: SQLDATE (str), EventCode (int), QuadClass (int), GoldsteinScale (float),
    ActionGeo_FullName (str), and SOURCEURL (str).
    Hint: You might find a constant in helpers.py useful.

    3. A new column called Text, which contains information parsed from the SOURCEURL column.

    4. Remove rows with missing or None values.

    5. Remove rows with duplicated SOURCEURL. If multiple rows share the same SOURCEURL,
    keep the row with the smallest GLOBALEVENTID.

    Args:
        data_folder (str): the folder containing the file
        filename (str): the name of the file to read

    Returns:
        pd.DataFrame, the cleaned dataframe

    """
    df = pd.DataFrame()
    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################
    # Hint: the resulting df should have 7 columns.
    # Hint: Do GDELT files contain a header row?

    GDELTFIELDNAMES = [
    "GLOBALEVENTID", "SQLDATE", "MonthYear", "Year", "FractionDate", "Actor1Code", "Actor1Name",
    "Actor1CountryCode", "Actor1KnownGroupCode", "Actor1EthnicCode", "Actor1Religion1Code", "Actor1Religion2Code",
    "Actor1Type1Code", "Actor1Type2Code", "Actor1Type3Code", "Actor2Code", "Actor2Name", "Actor2CountryCode",
    "Actor2KnownGroupCode", "Actor2EthnicCode", "Actor2Religion1Code", "Actor2Religion2Code", "Actor2Type1Code",
    "Actor2Type2Code", "Actor2Type3Code", "IsRootEvent", "EventCode", "EventBaseCode", "EventRootCode",
    "QuadClass", "GoldsteinScale", "NumMentions", "NumSources", "NumArticles", "AvgTone", "Actor1Geo_Type",
    "Actor1Geo_FullName", "Actor1Geo_CountryCode", "Actor1Geo_ADM1Code", "Actor1Geo_Lat", "Actor1Geo_Long",
    "Actor1Geo_FeatureID", "Actor2Geo_Type", "Actor2Geo_FullName", "Actor2Geo_CountryCode", "Actor2Geo_ADM1Code",
    "Actor2Geo_Lat", "Actor2Geo_Long", "Actor2Geo_FeatureID", "ActionGeo_Type", "ActionGeo_FullName",
    "ActionGeo_CountryCode", "ActionGeo_ADM1Code", "ActionGeo_Lat", "ActionGeo_Long", "ActionGeo_FeatureID",
    "DATEADDED", "SOURCEURL"
]

    file_path = os.path.join(data_folder, filename)

    # Define the columns we want
    columns = ["GLOBALEVENTID", "SQLDATE", "EventCode", "QuadClass", 
               "GoldsteinScale", "ActionGeo_FullName", "SOURCEURL"]
    
    # Get the column indices from GDELTFIELDNAMES
    usecols = [GDELTFIELDNAMES.index(col) for col in columns]
    
    # Read the raw file
    df = pd.read_csv(
        file_path,
        sep='\t',
        header=None,
        usecols=usecols,
        names=columns,
        dtype={
            'GLOBALEVENTID': str,
            'SQLDATE': str,
            'EventCode': str,
            'QuadClass': str,
            'GoldsteinScale': str,
            'ActionGeo_FullName': str,
            'SOURCEURL': str
        }
    )
    
    # First, ensure we have the correct data types
    df['EventCode'] = pd.to_numeric(df['EventCode'], errors='coerce').astype('Int64')
    df['QuadClass'] = pd.to_numeric(df['QuadClass'], errors='coerce').astype('Int64')
    df['GoldsteinScale'] = pd.to_numeric(df['GoldsteinScale'], errors='coerce')
    
    # Add the Text column
    df['Text'] = df['SOURCEURL'].apply(parse_url)
    
    # Remove rows with missing values in any column
    df = df.dropna()
    
    # Convert Int64 to regular int
    df['EventCode'] = df['EventCode'].astype(int)
    df['QuadClass'] = df['QuadClass'].astype(int)
    
    # Remove duplicates based on SOURCEURL, keeping the first occurrence (smallest GLOBALEVENTID)
    df = df.sort_values('GLOBALEVENTID').drop_duplicates(subset=['SOURCEURL'], keep='first')
    
    # Set the index to GLOBALEVENTID
    df = df.set_index('GLOBALEVENTID')

    ##############################################################################

    return df
