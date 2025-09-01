# 🎨 Skribbl.io Word Collector

A simple, fast, and collaborative web application built with Streamlit to create and manage custom word lists for games like Skribbl.io, Gartic Phone, or any other drawing/guessing game.

This tool allows users to create different "collections" (e.g., Movies, Science, Video Games) and add words to them. The data is stored locally in a `skribbl_data.json` file, making the application self-contained and easy to deploy.

## ✨ Features

- **Create Collections:** Easily create new categories for your word lists.
- **Add Words:** Quickly add words to any existing collection.
- **Duplicate Prevention:** The app automatically checks for duplicate words within a collection (case-insensitive) to keep lists clean.
- **Word Count Metric:** Each collection displays a real-time count of how many words it contains.
- **Simple & Clean UI:** Built with Streamlit for a straightforward and user-friendly experience.
- **Persistent Storage:** All collections and words are saved in a local `skribbl_data.json` file, so your data persists between sessions.

## 📂 Project Structure

The project is organized into two main parts: the Streamlit frontend and the data handling backend.

```
.
├── utils/
│   └── word_handling.py   # Class and logic for managing the JSON data file
├── app.py                 # The main Streamlit application file (UI)
├── skribbl_data.json      # The data file (auto-generated on first run)
├── .gitignore             # Standard git ignore file
└── README.md              # You are here!
```

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.7 or newer
- `pip` (Python package installer)

### Installation

1.  **Clone the repository (or download the files):**
    If you have the project files, you can skip this step.

    ```bash
    git clone [https://github.com/your-username/skribbl-word-collector.git](https://github.com/your-username/skribbl-word-collector.git)
    cd skribbl-word-collector
    ```

2.  **Create and activate a virtual environment (Recommended):**
    This keeps your project dependencies isolated.

    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    The only dependency for this project is Streamlit.
    ```bash
    pip install streamlit
    ```

## ▶️ How to Run the Application

With your virtual environment activated and Streamlit installed, run the following command in your terminal from the project's root directory:

```bash
streamlit run app.py
```

### Made for fun

## By Jatin Yadav
