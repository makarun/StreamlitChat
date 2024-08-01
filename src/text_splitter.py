from langchain.text_splitter import CharacterTextSplitter


class TextSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def split_text(self, text):
        return self.text_splitter.split_text(text)
