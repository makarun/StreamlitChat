import os
import streamlit as st
from dotenv import load_dotenv
from src.pdf_processor import PDFProcessor
from src.text_splitter import TextSplitter
from src.vector_store import VectorStore
from src.conversation_handler import ConversationHandler
from src.html_templates import css


resources_dir = "resources"
if not os.path.exists(resources_dir):
    os.makedirs(resources_dir)


def save_uploaded_files(uploaded_files):
    saved_files = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(resources_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(file_path)
    return saved_files


def get_all_files_in_resources():
    return [
        os.path.join(resources_dir, f)
        for f in os.listdir(resources_dir)
        if f.endswith(".pdf")
    ]


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")

    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        if st.session_state.conversation is not None:
            conversation_handler = ConversationHandler()
            conversation_handler.handle_user_input(user_question)
        else:
            st.warning("Please upload and process documents first.")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here or click 'Process'", accept_multiple_files=True
        )

        files = [
            f
            for f in os.listdir(resources_dir)
            if os.path.isfile(os.path.join(resources_dir, f))
        ]
        if files:
            st.subheader("Files from resource directory:")
            for f in files:
                st.write(f)
        else:
            st.write(
                "No files found in the resources directory. Please upload and process documents first."
            )

        if st.button("Process"):
            with st.spinner("Processing"):
                if pdf_docs:
                    save_uploaded_files(pdf_docs)

                all_files = get_all_files_in_resources()

                if all_files:
                    # Process the saved PDF files
                    raw_text = PDFProcessor.get_pdf_text(all_files)
                    text_splitter = TextSplitter()
                    text_chunks = text_splitter.split_text(raw_text)
                    vector_score = VectorStore()
                    vector_store_instance = vector_score.create_vectorstore(text_chunks)
                    st.session_state.conversation = (
                        ConversationHandler().create_conversation_chain(
                            vector_store_instance
                        )
                    )
                    st.success("Files processed successfully!")
                else:
                    st.warning("Please upload PDF files first.")


if __name__ == "__main__":
    main()
