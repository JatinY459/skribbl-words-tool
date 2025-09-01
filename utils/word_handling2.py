import streamlit as st
import pandas as pd
from st_gsheets_connection import GSheetsConnection

class WordCollectionManager:
    """
    Manages word collections by connecting to a Google Sheet as a database.

    This class handles reading, writing, and checking for duplicates,
    all by interacting directly with the Google Sheets API via Streamlit's
    connection utilities.
    """
    def __init__(self):
        """
        Initializes the connection to the Google Sheet.
        """
        try:
            # Establishes the connection using secrets stored in Streamlit.
            # It looks for a [connections.gsheets] section in your secrets.
            self.conn = st.connection("gsheets", type=GSheetsConnection)
            self.worksheet_name = "collections"
        except Exception as e:
            st.error("Failed to connect to Google Sheets. Check your secrets configuration.")
            st.stop()

    def _get_data(self) -> pd.DataFrame:
        """
        Private helper to fetch all data from the sheet.
        Caches the result for 60 seconds to avoid excessive API calls.
        
        Returns:
            pd.DataFrame: A DataFrame with all collections and words.
                          Returns an empty DataFrame if the sheet is empty or has issues.
        """
        try:
            # Read data from the specified worksheet.
            # The ttl parameter caches the data for the specified number of seconds.
            data = self.conn.read(worksheet=self.worksheet_name, ttl=60)
            # Ensure column names are consistent
            data.columns = [col.lower().replace(" ", "_") for col in data.columns]
            return data.dropna(how="all")
        except Exception:
            # If the sheet doesn't exist or is empty, return a correctly structured empty DataFrame
            return pd.DataFrame(columns=['collection_name', 'word'])

    def get_all_collections(self) -> dict:
        """
        Gets all unique collection names and the count of words in each.

        Returns:
            dict: A dictionary where keys are collection names (str)
                  and values are the word counts (int).
        """
        df = self._get_data()
        if df.empty or 'collection_name' not in df.columns:
            return {}
        
        # Group by collection name and count the number of words (rows) in each group
        collection_counts = df.groupby('collection_name').size().to_dict()
        return collection_counts

    def add_word(self, collection_name: str, word: str) -> str:
        """
        Adds a new word to a specified collection, checking for duplicates.

        Args:
            collection_name (str): The name of the collection.
            word (str): The word to add.

        Returns:
            str: A success or error message.
        """
        if not collection_name or not word:
            return "Error: Collection name and word cannot be empty."

        df = self._get_data()
        
        # Filter for the specific collection to check for duplicates
        collection_df = df[df['collection_name'].str.lower() == collection_name.lower()]

        # Check for duplicates (case-insensitive)
        existing_words = [str(w).lower() for w in collection_df['word']]
        if word.lower() in existing_words:
            return f"Error: The word '{word}' already exists in the '{collection_name}' collection."

        # If no duplicate, create a new row to append
        new_row = pd.DataFrame([{
            "collection_name": collection_name,
            "word": word
        }])

        try:
            # Update the sheet by appending the new row
            self.conn.update(worksheet=self.worksheet_name, data=pd.concat([df, new_row], ignore_index=True))
            return f"Success! Added '{word}' to '{collection_name}'."
        except Exception as e:
            return f"Error: Could not write to the Google Sheet. Details: {e}"

# Note: The 'add_collection' logic is now implicitly handled. A collection
# is "created" as soon as the first word is added to it. Your app.py can
# simply call add_word() to handle this.


