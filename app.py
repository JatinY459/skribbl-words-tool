# import streamlit as st
# from utils.word_handling import WordCollectionManager
# import time

# st.set_page_config(
#     page_title="Skribbl Word Collector",
#     page_icon="🎨",
#     layout="centered"
# )

# manager = WordCollectionManager('skribbl_data.json')

# if 'new_collection_name' not in st.session_state:
#     st.session_state.new_collection_name = ""

# st.title("🎨 Skribbl.io Word Collector")
# st.caption("A simple tool to collaboratively create custom word lists for games like Skribbl.io.")

# st.header("Create a New Collection")

# with st.form(key="create_collection_form", clear_on_submit=True):
#     new_collection_input = st.text_input(
#         "Enter new collection name",
#         placeholder="e.g., Video Games, Science, Disney Movies",
#         key="new_collection_name_input"
#     )
#     submitted = st.form_submit_button("Create Collection")

#     if submitted and new_collection_input:
#         if manager.add_collection(new_collection_input):
#             st.success(f"Collection '{new_collection_input}' was created successfully!")
#             time.sleep(1)
#             st.rerun()
#         else:
#             st.error(f"Collection '{new_collection_input}' already exists.")

# st.divider()

# # Section: Existing Collections 
# st.header("Existing Collections")

# collections = manager.get_all_collections()

# if not collections:
#     st.info("No collections found. Create one above to get started!")
# else:
#     collections.sort()
    
#     for collection_name in collections:
#         words = manager.get_words_in_collection(collection_name)
#         word_count = len(words) if words is not None else 0

#         with st.container(border=True):
#             col1, col2 = st.columns([3, 1])

#             with col1:
#                 st.subheader(f"{collection_name.replace('-', ' ').title()}")

#             with col2:
#                 st.metric(label="Words", value=word_count)

#             with st.form(key=f"add_word_form_{collection_name}", clear_on_submit=True):
#                 word_col, btn_col = st.columns([3,1])
#                 with word_col:
#                     new_word_input = st.text_input(
#                         "Add a new word",
#                         placeholder="Type a word and press 'Add'",
#                         label_visibility="collapsed",
#                         key=f"new_word_input_{collection_name}"
#                     )
#                 with btn_col:
#                     add_word_submitted = st.form_submit_button("Add Word")

#                 if add_word_submitted and new_word_input:
#                     if manager.add_word(collection_name, new_word_input):
#                         st.rerun()
#                     else:
#                         st.toast(f"'{new_word_input}' is already in this collection!", icon="⚠️")


# st.divider()
# col1, col2, col3 = st.columns([1, 2, 1])
# with col2:
#     col2.markdown("""<div style="font-size:1.5rem;">Made for Fun</div>""", unsafe_allow_html=True)
#     col2.markdown("""<div style="font-size:2rem;">By Jatin Yadav</div>""", unsafe_allow_html=True)



# new one: #######################################

import streamlit as st
from utils.word_handling import WordCollectionManager
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Skribbl Word Collector",
    page_icon="🎨",
    layout="centered"
)

# --- Initialization ---
manager = WordCollectionManager('skribbl_data.json')

# Initialize session state for the input field if it doesn't exist
if 'new_collection_name' not in st.session_state:
    st.session_state.new_collection_name = ""

# --- Header ---
st.title("🎨 Skribbl.io Word Collector")
st.caption("A simple tool to collaboratively create custom word lists for games like Skribbl.io.")

# --- Create New Collection Form ---
st.header("Create a New Collection")
with st.form(key="create_collection_form", clear_on_submit=True):
    new_collection_input = st.text_input(
        "Enter new collection name",
        placeholder="e.g., Video Games, Science, Disney Movies",
        key="new_collection_name_input"
    )
    submitted = st.form_submit_button("Create Collection")

    if submitted and new_collection_input:
        if manager.add_collection(new_collection_input):
            st.success(f"Collection '{new_collection_input}' was created successfully!")
            time.sleep(1) # A short delay to let the user see the message
            st.rerun()
        else:
            st.error(f"Collection '{new_collection_input}' already exists.")

st.divider()

# --- Existing Collections Section ---
st.header("Existing Collections")

collections = manager.get_all_collections()

if not collections:
    st.info("No collections found. Create one above to get started!")
else:
    collections.sort() # Display collections in alphabetical order
    
    for collection_name in collections:
        words = manager.get_words_in_collection(collection_name)
        word_count = len(words) if words is not None else 0

        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                # Display collection name with better formatting
                st.subheader(f"{collection_name.replace('-', ' ').title()}")
            
            with col2:
                st.metric(label="Words", value=word_count)

            # --- NEW: View/Edit Words Expander ---
            with st.expander("View / Edit Words"):
                if not words:
                    st.write("This collection is empty. Add a word below!")
                else:
                    # Display each word with a remove button
                    for word in words:
                        word_col, button_col = st.columns([4, 1])
                        with word_col:
                            st.markdown(f"- {word}")
                        with button_col:
                            # Unique key for each button is crucial
                            if st.button("Remove", key=f"remove_{collection_name}_{word}", use_container_width=True):
                                manager.remove_word(collection_name, word)
                                st.toast(f"Removed '{word}'!", icon="🗑️")
                                time.sleep(1) # Short delay for toast visibility
                                st.rerun()

            # --- Add Word Form ---
            with st.form(key=f"add_word_form_{collection_name}", clear_on_submit=True):
                word_col, btn_col = st.columns([3,1])
                with word_col:
                    new_word_input = st.text_input(
                        "Add a new word",
                        placeholder="Type a word and press 'Add'",
                        label_visibility="collapsed",
                        key=f"new_word_input_{collection_name}"
                    )
                with btn_col:
                    add_word_submitted = st.form_submit_button("Add Word")

                if add_word_submitted and new_word_input:
                    if manager.add_word(collection_name, new_word_input):
                        st.rerun() # Rerun to update the word count and list
                    else:
                        st.toast(f"'{new_word_input}' is already in this collection!", icon="⚠️")


# --- Footer ---
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""<div style="text-align: center; font-size:1.2rem;">Made for Fun</div>""", unsafe_allow_html=True)
    st.markdown("""<div style="text-align: center; font-size:1.5rem;">By Jatin Yadav</div>""", unsafe_allow_html=True)