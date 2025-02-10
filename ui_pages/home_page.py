import gradio as gr
from ui_pages.base_page import BasePage
from controllers.objective_controller import create_objective, get_objectives_by_user
from sqlalchemy.orm import Session
from .learning_page import LearningPage  # type: ignore


class HomePage(BasePage):
    def __init__(self, db: Session, learning_page: LearningPage):
        super().__init__()
        self.db = db
        self.learning_page = learning_page
        self.user_id = 1
        self.objective_id = None

        with gr.Blocks() as self.interface:
            self.tab_home = gr.TabItem("Home", id="home")  # 添加 id
            self.tab_learning = gr.TabItem("Learning", id="learning", visible=False)  # 初始时不可见

            with self.tab_home:
                gr.Markdown("# GrowledgePilot")
                with gr.Tabs():
                    with gr.TabItem("Dashboard"):
                        self.create_dashboard_tab()

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

        objective = create_objective(db=self.db, user_id=self.user_id, name=name, description=description,
                                     priority=priority, current_level=current_level,
                                     target_level=target_level)  # type: ignore
        return f"Objective '{objective.name}' added successfully."  # type: ignore

    def refresh_objectives(self):
        objectives = get_objectives_by_user(db=self.db, user_id=self.user_id)  # type: ignore
        if objectives:
            data = []
            for obj in objectives:
                data.append([obj.id, obj.name, obj.description, obj.priority, obj.current_level, obj.target_level])
            return data
        else:
            return []

    def start_learning(self, objective_selected):
        if objective_selected:
            try:
                objective_id = int(objective_selected)
            except:
                return "objective id must be a integer"
            self.learning_page.objective_id = objective_id
            self.learning_page.init_agent()

            return gr.update(visible=False), gr.update(visible=True)  # 更新 visible 属性
        return gr.update(visible=True), gr.update(visible=False)
