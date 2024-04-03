import os
import json
from datetime import datetime as dt
import gradio as gr
import auto_ta


def log_qa(q_str, a_str):
    log = {'question': q_str, 'answer': a_str}

    with open(f'logs/{dt.now():%Y%m%d_%H%M%S}.json', 'w') as f:
        json.dump(log, f)


def log_good_ans(q_str, a_str):
    log = {'question': q_str, 'answer': a_str}

    with open(f'logs/good_{dt.now():%Y%m%d_%H%M%S}.json', 'w') as f:
        json.dump(log, f)

    return gr.update(interactive=False)


def main():
    query_engine = auto_ta.Gemma2BQueryEngine('corpus/')
    theme = gr.themes.Default(spacing_size='lg', text_size='lg')

    with gr.Blocks(theme=theme) as qabot:
        qbox = gr.Textbox(label='Enter your question')
        abox = gr.Textbox(label='Answer', interactive=False, autoscroll=False, max_lines=12)

        with gr.Row():
            submit_btn = gr.Button('Submit', size='sm')
            clear_btn = gr.ClearButton(components=[qbox, abox], size='sm')
            flag_btn = gr.Button('Good Response', size='sm', interactive=False)

        gr.on(
            triggers=[qbox.submit, submit_btn.click], fn=query_engine.query,
            inputs=qbox, outputs=abox
        )
        qbox.change(lambda: gr.update(interactive=True), outputs=flag_btn)
        abox.change(log_qa, inputs=[qbox, abox])
        flag_btn.click(log_good_ans, inputs=[qbox, abox], outputs=flag_btn)

    qabot.launch(server_name='0.0.0.0', server_port=int(os.environ['SERVER_PORT']))


if __name__ == '__main__':
    main()
