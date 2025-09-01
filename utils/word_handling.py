import json
import os

class WordCollectionManager:
    """
    Manages a collection of words stored in a single JSON file.

    This class handles all operations like adding/removing collections and words,
    ensuring the JSON file is always well-formatted and preventing duplicates.
    """

    def __init__(self, filepath='skribbl_data.json'):
        """
        Initializes the manager with the path to the JSON data file.

        Args:
            filepath (str): The path to the json file where data is stored.
                            Defaults to 'skribbl_data.json'.
        """
        self.filepath = filepath
        self._initialize_file()

    def _initialize_file(self):
        """
        Ensures the JSON file exists and contains a valid empty dictionary if new.
        This prevents errors on first run or if the file gets corrupted.
        """
        if not os.path.exists(self.filepath):
            # Create the file with an empty JSON object if it doesn't exist
            self._write_data({})
        else:
            # If the file exists but is empty, initialize it
            if os.path.getsize(self.filepath) == 0:
                self._write_data({})

    def _read_data(self):
        """
        Reads the data from the JSON file.

        Returns:
            dict: The data from the JSON file as a Python dictionary.
                  Returns an empty dictionary if the file is empty or corrupt.
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If the file is corrupt or not found, return an empty dict
            # to prevent the app from crashing.
            return {}

    def _write_data(self, data):
        """
        Writes a dictionary to the JSON file.

        Args:
            data (dict): The Python dictionary to write to the file.
        """
        with open(self.filepath, 'w', encoding='utf-8') as f:
            # indent=4 makes the JSON file human-readable
            json.dump(data, f, indent=4)

    def add_collection(self, collection_name):
        """
        Adds a new, empty collection.

        Args:
            collection_name (str): The name for the new collection.

        Returns:
            bool: True if the collection was added, False if it already exists.
        """
        data = self._read_data()
        if collection_name in data:
            print(f"Error: Collection '{collection_name}' already exists.")
            return False
        
        data[collection_name] = []
        self._write_data(data)
        print(f"Success: Collection '{collection_name}' created.")
        return True

    def add_word(self, collection_name, word):
        """
        Adds a word to a specified collection, checking for duplicates (case-insensitive).

        Args:
            collection_name (str): The collection to add the word to.
            word (str): The word to add.

        Returns:
            bool: True if the word was added, False otherwise (e.g., duplicate or collection not found).
        """
        data = self._read_data()
        if collection_name not in data:
            print(f"Error: Collection '{collection_name}' not found.")
            return False

        # Case-insensitive check for duplicates
        if any(existing_word.lower() == word.lower() for existing_word in data[collection_name]):
            print(f"Info: Word '{word}' already exists in '{collection_name}'.")
            return False

        data[collection_name].append(word)
        data[collection_name].sort() # Keep the list sorted alphabetically
        self._write_data(data)
        print(f"Success: Added '{word}' to '{collection_name}'.")
        return True

    def remove_word(self, collection_name, word):
        """
        Removes a word from a specified collection (case-insensitive).

        Args:
            collection_name (str): The collection to remove the word from.
            word (str): The word to remove.

        Returns:
            bool: True if the word was removed, False if it wasn't found.
        """
        data = self._read_data()
        if collection_name not in data:
            print(f"Error: Collection '{collection_name}' not found.")
            return False

        # Find the exact word to remove, ignoring case
        word_to_remove = None
        for existing_word in data[collection_name]:
            if existing_word.lower() == word.lower():
                word_to_remove = existing_word
                break

        if word_to_remove:
            data[collection_name].remove(word_to_remove)
            self._write_data(data)
            print(f"Success: Removed '{word_to_remove}' from '{collection_name}'.")
            return True
        else:
            print(f"Error: Word '{word}' not found in '{collection_name}'.")
            return False

    def get_all_collections(self):
        """
        Retrieves a list of all collection names.

        Returns:
            list: A list of strings with all collection names.
        """
        data = self._read_data()
        return list(data.keys())

    def get_words_in_collection(self, collection_name):
        """
        Retrieves all words within a specific collection.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            list or None: A list of words if the collection exists, otherwise None.
        """
        data = self._read_data()
        return data.get(collection_name)

# --- Example Usage ---
if __name__ == "__main__":
    # 1. Create an instance of the manager
    #    This will automatically create 'skribbl_data.json' if it doesn't exist
    manager = WordCollectionManager()

    # 2. Add some collections
    print("\n--- Adding Collections ---")
    manager.add_collection("movies")
    manager.add_collection("science")
    manager.add_collection("movies") # Try to add a duplicate collection

    # 3. Add words to a collection
    print("\n--- Adding Words ---")
    manager.add_word("movies", "Inception")
    manager.add_word("movies", "Parasite")
    manager.add_word("science", "Galaxy")
    manager.add_word("movies", "inception") # Try to add a duplicate word (case-insensitive)
    manager.add_word("does_not_exist", "word") # Try to add to a non-existent collection

    # 4. View the current data
    print("\n--- Current State ---")
    all_collections = manager.get_all_collections()
    print(f"All Collections: {all_collections}")

    movie_words = manager.get_words_in_collection("movies")
    print(f"Words in 'movies': {movie_words}")

    # 5. Remove a word
    print("\n--- Removing Words ---")
    manager.remove_word("movies", "Parasite")
    manager.remove_word("science", "blackhole") # Try to remove a word that isn't there

    # 6. View the final data
    print("\n--- Final State ---")
    final_movie_words = manager.get_words_in_collection("movies")
    print(f"Final words in 'movies': {final_movie_words}")
