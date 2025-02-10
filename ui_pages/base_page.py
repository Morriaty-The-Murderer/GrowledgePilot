# -*- coding: utf-8 -*-
from settings import GRADIO_HOST, GRADIO_PORT


class BasePage:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def render(self):
        for component in self.components:
            if isinstance(component, BasePage):
                component.render()
            # else:
            #     component.render() # gradio component has render method

    def launch(self):
        if self.interface:  # 避免重复 launch
            self.interface.launch(server_name=GRADIO_HOST, server_port=GRADIO_PORT, reload=True)
