from llama_index.core import SimpleDirectoryReader
from transformers import logging

from auto_ta.retrievers import DefaultRetriever
from auto_ta.readers import SummarizerReader, DefaultLLMReader, StableLM2Reader

logging.set_verbosity_error()


class QueryEngine:
    def __init__(self, retriever, reader):
        self.retriever = retriever
        self.reader = reader

    def query(self, query_str):
        rtvd_nodes = self.retriever.retrieve(query_str)
        context_str = '\n\n'.join(node.get_content() for node in rtvd_nodes)

        if len(rtvd_nodes) == 0:
            return 'Sorry I cannot find relevant information to answer that.'

        answer_str = self.reader.answer(context_str, query_str)

        sources_str = '\n\n'.join(
            f'[{i}] {node.metadata["file_name"]} | Score={node.score:.4f}\n{node.text}'
            for i, node in enumerate(rtvd_nodes, start=1)
        )

        response = f'{answer_str}\n\nSources:\n{sources_str}'

        return response


class SummaryQueryEngine(QueryEngine):
    def __init__(self, corpus_path, top_k=5):
        corpus = SimpleDirectoryReader(corpus_path, recursive=True).load_data()
        retriever = DefaultRetriever(corpus, top_k)
        reader = SummarizerReader()
        super().__init__(retriever, reader)

    def __str__(self):
        return f'SummaryQueryEngine(\n\tretriever={self.retriever},\n\treader={self.reader}\n)'



class LLMQueryEngine(QueryEngine):
    def __init__(self, corpus_path, top_k=5):
        corpus = SimpleDirectoryReader(corpus_path, recursive=True).load_data()
        retriever = DefaultRetriever(corpus, top_k)
        reader = StableLM2Reader()  # DefaultLLMReader()
        super().__init__(retriever, reader)

    def __str__(self):
        return f'LLMQueryEngine(\n\tretriever={self.retriever},\n\treader={self.reader}\n)'
