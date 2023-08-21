import modules.scripts as scripts
import gradio as gr
import os
import requests
from modules import images, script_callbacks
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state


class ExtensionTemplateScript(scripts.Script):
    # Extension title in menu UI
    def title(self):
        print('----------------custom extension titile')
        return "save state"

    # Decide to show menu in txt2img or img2img
    # - in "txt2img" -> is_img2img is `False`
    # - in "img2img" -> is_img2img is `True`
    #
    # below code always show extension menu
    def show(self, is_img2img):
        print('----------------custom extension show')
        # return True
        return scripts.AlwaysVisible

    # Setup menu ui detail
    def ui(self, is_img2img):
        print('----------------custom extension ui')
        with gr.Accordion('save state', open=False):
            with gr.Row():
                textbox = gr.Textbox(label="文件名前缀", placeholder="请输入")
        # TODO: add more UI components (cf. https://gradio.app/docs/#components)
        return [textbox]

    # Extension main process
    # Type: (StableDiffusionProcessing, List<UI>) -> (Processed)
    # args is [StableDiffusionProcessing, UI1, UI2, ...]
    def run(self, p, textbox):
        print('----------------custom extension run')
        print(p.prompt)
        print(p.negative_prompt)
        print(p.script_args)
        for script in p.scripts.scripts:
            print(script.title())
        # TODO: get UI info through UI object angle, checkbox
        proc = process_images(p)
        # TODO: add image edit process via Processed object proc
        return proc

    def postprocess(self, p, processed, *args):
        print('----------------custom extension postprocess')
        # response = requests.post('', json=data)
        response = requests.get('https://www.baidu.com')
        print(response.status_code)
        print(response.text)
        print(processed)
        print(args[0])
        print(p.prompt)
        print(p.negative_prompt)
        print(p.script_args)
        for script in p.scripts.scripts:
            scriptTitle = script.title()
            print(scriptTitle)
            scriptArgs = p.script_args[script.args_from:script.args_to]
            print(scriptArgs)
            if scriptTitle == 'ControlNet':
                for c in scriptArgs:
                    print(c.enabled)
                    print(c.image)
                    print(c.get_modules_detail())
                    print(c.__dict__)
        return p
