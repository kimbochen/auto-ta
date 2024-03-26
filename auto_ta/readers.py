from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.prompts import PromptTemplate
from transformers import pipeline


class SummarizerReader:
    def __init__(self, **kwargs):
        self.summarizer = pipeline('summarization', model='ainize/bart-base-cnn')
        self.summarizer_kwargs = dict(
            max_length=130, min_length=30, do_sample=False
        )
        self.summarizer_kwargs.update(kwargs)

    def answer(self, context_str, query_str):
        summary = self.summarizer(context_str, **self.summarizer_kwargs)
        return summary[0]['summary_text']


class LLMReader:
    def __init__(self, llm_name, prompt_tmpl, **kwargs):
        self.llm_name = llm_name
        self.llm = HuggingFaceLLM(
            model_name=llm_name,
            tokenizer_name=llm_name,
            **kwargs
        )
        self.prompt_tmpl = prompt_tmpl

    def answer(self, context_str, query_str):
        prompt = self.prompt_tmpl.format(context_str=context_str, query_str=query_str)
        answer = self.llm.complete(prompt)
        return answer

    def __str__(self):
        return f'LLMReader(llm_name={self.llm_name})'


class DefaultLLMReader(LLMReader):
    def __init__(self):
        llm_name = 'stabilityai/stablelm-zephyr-3b'
        prompt_tmpl = PromptTemplate('''\
<|user|>
Context information is below.
---------------------
{context_str}
---------------------
You are a teaching assistant that clarifies students' questions about the assignment.
Given the context information and not prior knowledge, answer the query only with the context information.
Respond "Sorry I cannot answer that" if no relevant information is in the context.
Query: {query_str}
<|endoftext|>
<|assistant|>
''')
        super().__init__(
            llm_name, prompt_tmpl,
            context_window=3900,
            max_new_tokens=256,
            device_map='cuda',
            model_kwargs={'trust_remote_code': True}
        )


class StableLM2Reader(LLMReader):
    def __init__(self):
        llm_name = 'stabilityai/stablelm-2-zephyr-1_6b'
        prompt_tmpl = PromptTemplate('''\
<|user|>
Context information is below.
---------------------
{context_str}
---------------------
You are a teaching assistant that clarifies students' questions about the assignment.
Given the context information and not prior knowledge, answer the query only with the context information.
Respond "Sorry I cannot answer that" if no relevant information is in the context.
Query: {query_str}<|endoftext|>
<|assistant|>
''')
        super().__init__(
            llm_name, prompt_tmpl,
            max_new_tokens=256,
            device_map='cuda',
            model_kwargs={'trust_remote_code': True}
        )
