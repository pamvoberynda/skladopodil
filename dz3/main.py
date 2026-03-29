import gradio as gr
from password_gen import create_password

with gr.Blocks() as demo:
    inp = gr.Textbox(label="Введіть своє імʼя латиницею:")

    btn = gr.Button("Створити пароль")
    out = gr.Textbox(label="Рекомендований для вас пароль:")

    btn.click(fn=create_password, inputs=inp, outputs=out)


demo.launch()