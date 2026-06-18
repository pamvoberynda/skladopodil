import gradio as gr
from syllabizer import separate_syllables

def cr_syllables(text: str) -> str:
    output = separate_syllables(text)
    return output

copy_to_clipboard_js = """
(text) => {
    navigator.clipboard.writeText(text).then(() => {
        alert("Copied to clipboard!");
    }).catch(err => {
        console.error("Failed to copy: ", err);
    });
}
"""

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label="Enter the string")
            btn_syllabize = gr.Button("Separate syllables")
        with gr.Column():
            out = gr.Textbox(label="There will be displayed the syllables")
            btn_copy = gr.Button("Copy")
    btn_syllabize.click(fn=cr_syllables, inputs=inp, outputs=out)
    btn_copy.click(fn=None, inputs=[inp], outputs=None, js=copy_to_clipboard_js)
demo.launch()