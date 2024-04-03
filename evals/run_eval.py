import sys
import json

from llama_index.core import SimpleDirectoryReader
from transformers import logging
from tqdm import tqdm

from auto_ta.readers import *
from auto_ta.retrievers import *
from auto_ta.query_engines import QueryEngine

logging.set_verbosity_error()
CORPUS = SimpleDirectoryReader('../corpus/', recursive=True).load_data()


class EnsBase_StableLM2_1_6B(QueryEngine):
    def __init__(self):
        retriever = EnsembleRetriever('base', CORPUS, top_k=5)
        reader = StableLM2Reader()
        super().__init__(retriever, reader)


class EnsBase_StableLM_3B(QueryEngine):
    def __init__(self):
        retriever = EnsembleRetriever('base', CORPUS, top_k=5)
        reader = StableLM3BReader()
        super().__init__(retriever, reader)


class EnsSmall_Gemm2B(QueryEngine):
    def __init__(self):
        retriever = EnsembleRetriever('small', CORPUS, top_k=5)
        reader = Gemma2BReader()
        super().__init__(retriever, reader)


class EnsBase_Gemm2B(QueryEngine):
    def __init__(self):
        retriever = EnsembleRetriever('base', CORPUS, top_k=5)
        reader = Gemma2BReader()
        super().__init__(retriever, reader)


EvalQueryEngine = EnsBase_Gemm2B  # Query engine evaluated
EvalQueryEngine.__str__ = lambda self: f'{type(self).__name__}(\n\tretriever={self.retriever},\n\treader={self.reader}\n)'


def main():
    eval_questions_path = './cs203_eval.json'
    results_path = sys.argv[1]
    query_engine = EvalQueryEngine()

    print(f'Evaluating query engine:\n{query_engine}')

    with open(eval_questions_path) as f:
        eval_questions = json.load(f)

    results = []

    for eval_q in tqdm(eval_questions):
        response = query_engine.query(eval_q['query'])
        result = {
            'response': response,
            'good_retv': None,
            'refuse': None,
            'good_resp': None,
            'comment': None
        }
        result.update(eval_q)
        results.append(result)

    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)


if __name__ == '__main__':
    main()
