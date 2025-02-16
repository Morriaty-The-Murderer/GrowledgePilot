import gradio as gr
from ui_pages.base_page import BasePage
from ai_agents.learning_agent import LearningAgent
from sqlalchemy.orm import Session
from controllers import learning_controller
from controllers.user_controller import UserController
from ai_agents import prompt_templates


class LearningPage(BasePage):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.user_controller = UserController(db)
        self.learning_agent = None
        self.objective_id = None
        self.learning_session_id = None
        self.user_id = None

        with gr.Blocks() as self.interface:  # 将 self.interface 赋值给 gr.Blocks() 实例
            self.render_content()  # 将内容渲染移到 render_content 方法中

    def render_content(self):
        gr.Markdown("# Learning Page")
        with gr.Row():
            self.user_input = gr.Textbox(label="Your Input")
            self.send_button = gr.Button("Send")
        with gr.Row():
            self.ai_output = gr.Markdown(label="AI Output")

        self.send_button.click(
            self.respond,
            inputs=[self.user_input],
            outputs=[self.ai_output]
        )

        self.end_session_button = gr.Button("End Session")
        self.end_session_button.click(self.end_session, inputs=[], outputs=[])

    def init_agent(self, user_id: int = None):
        if not self.learning_agent:
            if self.objective_id:
                self.user_id = user_id or self.user_id
                if not self.user_id:
                    return False
                    
                user = self.user_controller.get_user(self.user_id)
                if not user:
                    return False

                self.learning_agent = LearningAgent(
                    user_id=self.user_id,
                    objective_id=self.objective_id,
                    db=self.db
                )

                # Create learning session
                self.learning_session_id = learning_controller.create_learning_session(
                    db=self.db,
                    user_id=self.user_id,
                    objective_id=self.objective_id,
                    content=f"Start learning objective {self.objective_id}",
                    ai_prompt=prompt_templates.GENERAL_LEARNING_PROMPT
                ).id

    def respond(self, user_input):
        if self.learning_agent:
            response = self.learning_agent.generate_learning_response(
                user_input,
                prompt_templates.GENERAL_LEARNING_PROMPT
            )

            # 更新学习会话内容
            if self.learning_session_id:
                learning_controller.end_learning_session(
                    db=self.db,  # type: ignore
                    session_id=self.learning_session_id,
                    notes=f"{user_input}\n{response}"
                )

            return response
        return "Learning agent not initialized."

    def end_session(self):
        if self.learning_session_id:
            learning_controller.end_learning_session(db=self.db, session_id=self.learning_session_id,
                                                     notes="End Session")  # type: ignore
