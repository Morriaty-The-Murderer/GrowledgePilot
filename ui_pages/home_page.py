import gradio as gr
from sqlalchemy.orm import Session

from controllers.meta_prompt_controller import MetaPromptController
from controllers.objective_controller import ObjectiveController
from controllers.user_controller import UserController
from ui_pages.base_page import BasePage
from .learning_page import LearningPage  # type: ignore


class HomePage(BasePage):
    def __init__(self, db: Session, learning_page: LearningPage):
        super().__init__()
        self.db = db
        self.learning_page = learning_page
        self.user_id = None
        self.objective_id = None
        self.user_controller = UserController(db)
        self.objective_controller = ObjectiveController(db)
        self.meta_prompt_controller = MetaPromptController(db)

        with gr.Blocks() as self.interface:
            self.tab_home = gr.TabItem("Home", id="home")
            self.tab_register = gr.TabItem("Register", id="register", visible=True)
            self.tab_learning = gr.TabItem("Learning", id="learning", visible=False)

            with self.tab_home:
                gr.Markdown("# GrowledgePilot")
                with gr.Tabs():
                    with gr.TabItem("Dashboard"):
                        self.create_dashboard_tab()

            with self.tab_register:
                self.create_registration_tab()

            with self.tab_learning:
                self.learning_page.render_content()  # 将 LearningPage 的内容渲染到这里

    def create_dashboard_tab(self):
        with gr.Row():
            self.objective_name = gr.Textbox(label="Objective Name")
            self.objective_description = gr.Textbox(label="Description")
            self.objective_priority = gr.Number(label="Priority", precision=0)
            self.objective_current_level = gr.Textbox(label="Current Level")
            self.objective_target_level = gr.Textbox(label="Target Level")
            self.add_objective_button = gr.Button("Add Objective")
            self.objective_message = gr.Markdown()

        with gr.Row():
            self.objectives_list = gr.Dataframe(
                headers=["id", "name", "description", "priority", "current_level", "target_level"],
                label="Your Objectives")
            self.refresh_objectives_button = gr.Button("Refresh Objectives")

        with gr.Row():
            self.start_learning_button = gr.Button("Start Learning")
            self.objective_selected = gr.Textbox(label="Objective Selected")

        self.add_objective_button.click(
            self.add_objective,
            inputs=[self.objective_name, self.objective_description, self.objective_priority,
                    self.objective_current_level, self.objective_target_level],
            outputs=[self.objective_message]
        )

        self.refresh_objectives_button.click(
            self.refresh_objectives,
            inputs=[],
            outputs=[self.objectives_list]
        )
        self.start_learning_button.click(
            self.start_learning,
            inputs=[self.objective_selected],
            outputs=[self.tab_home, self.tab_learning]  # 改为更新两个 TabItem 的 visible 属性
        )

    def add_objective(self, name, description, priority, current_level, target_level):
        try:
            priority = int(priority)
        except ValueError:
            return "Priority must be an integer."

        objective = self.objective_controller.create_objective(
            user_id=self.user_id,
            name=name,
            description=description,
            priority=priority,
            current_level=current_level,
            target_level=target_level
        )
        return f"Objective '{objective.name}' added successfully."

    def refresh_objectives(self):
        objectives = self.objective_controller.get_objectives_by_user(self.user_id)
        if objectives:
            data = []
            for obj in objectives:
                data.append([obj.id, obj.name, obj.description, obj.priority,
                             obj.current_level, obj.target_level])
            return data
        else:
            return []

    def create_registration_tab(self):
        with gr.Column():
            gr.Markdown("## User Registration")
            self.reg_name = gr.Textbox(label="Name")
            self.reg_age = gr.Number(label="Age", precision=0)
            self.reg_occupation = gr.Textbox(label="Occupation")
            self.reg_language = gr.Dropdown(
                label="Preferred Language",
                choices=["English", "Chinese", "Spanish", "Other"]
            )
            self.reg_submit = gr.Button("Register")
            self.reg_message = gr.Markdown()

            with gr.Group():
                gr.Markdown("### Learning Preferences")
                self.learning_style = gr.Radio(
                    label="Preferred Learning Style",
                    choices=["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
                    visible=False
                )
                self.learning_goals = gr.CheckboxGroup(
                    label="Learning Goals",
                    choices=["Technical Skills", "Soft Skills", "Academic", "Professional"],
                    visible=False
                )
                self.prompt_preview = gr.Textbox(
                    label="Personalized Prompt Preview",
                    interactive=False,
                    visible=False
                )
                self.progress_bar = gr.Slider(
                    label="Registration Progress",
                    minimum=0,
                    maximum=100,
                    value=0,
                    interactive=False
                )

        self.reg_submit.click(
            self.handle_registration,
            inputs=[self.reg_name, self.reg_age, self.reg_occupation, self.reg_language],
            outputs=[self.reg_message, self.learning_style, self.learning_goals,
                     self.prompt_preview, self.progress_bar]
        )

    def handle_registration(self, name, age, occupation, language):
        try:
            user = self.user_controller.create_user(
                name=name,
                age=int(age),
                occupation=occupation,
                language_preference=language
            )
            self.user_id = user.id

            # Initialize meta prompt session
            session = self.meta_prompt_controller.create_session(user.id)
            progress = self.meta_prompt_controller.get_session_progress(session.id)

            return (
                f"Registration successful! Welcome {name}!",
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                progress["progress_percentage"]
            )
        except Exception as e:
            return (
                f"Registration failed: {str(e)}",
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                0
            )

    def start_learning(self, objective_selected):
        if not self.user_id:
            return gr.update(visible=False), gr.update(visible=False)

        if objective_selected:
            try:
                objective_id = int(objective_selected)
            except:
                return "objective id must be a integer"
            self.learning_page.objective_id = objective_id
            self.learning_page.init_agent()

            return gr.update(visible=False), gr.update(visible=True)
        return gr.update(visible=True), gr.update(visible=False)
