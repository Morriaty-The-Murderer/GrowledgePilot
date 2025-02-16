# -*- coding: utf-8 -*-
from typing import Optional, Dict
import gradio as gr
from fastapi import Depends
from sqlalchemy.orm import Session

from utils.database import get_db
from .base_page import BasePage
from controllers.meta_prompt_controller import MetaPromptController, PromptCollectionStep


class MetaPromptPage(BasePage):
    def __init__(self, db: Session = Depends(get_db)):
        super().__init__()
        self.db = db
        self.controller = MetaPromptController(db)
        self.current_session_id = None
        self.current_step = None

    def render_content(self, container=None):
        with gr.Blocks() as self.interface:
            self.progress_bar = gr.Slider(
                minimum=0,
                maximum=100,
                value=0,
                label="Progress",
                interactive=False
            )
            
            with gr.Column(visible=True) as self.step_container:
                self.step_heading = gr.Markdown("### Let's get started!")
                
                # Learning Style Form
                with gr.Column(visible=False) as self.learning_style_form:
                    gr.Markdown("### What's your preferred way of learning?")
                    self.learning_style = gr.Radio(
                        choices=["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
                        label="Learning Style"
                    )
                    self.learning_style_submit = gr.Button("Next")
                
                # Goals Form
                with gr.Column(visible=False) as self.goals_form:
                    gr.Markdown("### What are your learning goals?")
                    self.short_term_goals = gr.TextArea(
                        label="Short-term Goals",
                        placeholder="What do you want to achieve in the next few months?"
                    )
                    self.long_term_goals = gr.TextArea(
                        label="Long-term Goals",
                        placeholder="What are your ultimate learning objectives?"
                    )
                    self.goals_submit = gr.Button("Next")
                
                # Interests Form
                with gr.Column(visible=False) as self.interests_form:
                    gr.Markdown("### What topics interest you?")
                    self.interests = gr.CheckboxGroup(
                        choices=[
                            "Technology", "Science", "Arts", "Business",
                            "Languages", "History", "Mathematics", "Other"
                        ],
                        label="Areas of Interest"
                    )
                    self.other_interests = gr.TextArea(
                        label="Other Interests",
                        placeholder="Please specify any other interests..."
                    )
                    self.interests_submit = gr.Button("Next")
                
                # Review Step
                with gr.Column(visible=False) as self.review_form:
                    gr.Markdown("### Review Your Preferences")
                    self.summary = gr.Markdown()
                    self.prompt_preview = gr.TextArea(
                        label="Generated Learning Prompt",
                        interactive=False
                    )
                    with gr.Row():
                        self.edit_button = gr.Button("Edit Preferences")
                        self.confirm_button = gr.Button("Confirm & Continue")
                
            self.step_message = gr.Markdown()
            
            # Event handlers
            self.learning_style_submit.click(
                fn=self.handle_learning_style,
                inputs=[self.learning_style],
                outputs=[self.step_message]
            )
            
            self.goals_submit.click(
                fn=self.handle_goals,
                inputs=[self.short_term_goals, self.long_term_goals],
                outputs=[self.step_message]
            )
            
            self.interests_submit.click(
                fn=self.handle_interests,
                inputs=[self.interests, self.other_interests],
                outputs=[self.step_message]
            )
            
            self.edit_button.click(
                fn=self.reset_session,
                outputs=[
                    self.learning_style_form,
                    self.goals_form,
                    self.interests_form,
                    self.review_form,
                    self.progress_bar,
                    self.step_message
                ]
            )
            
            self.confirm_button.click(
                fn=self.complete_session,
                outputs=[self.step_message]
            )

    def start_session(self, user_id: int):
        """Initialize a new meta prompt session"""
        session = self.controller.create_session(user_id)
        self.current_session_id = session.id
        self.current_step = PromptCollectionStep.INIT
        progress = self.controller.get_session_progress(session.id)
        return self.update_interface_for_step(progress["current_step"])
    
    def handle_learning_style(self, style: str) -> Dict:
        """Process learning style input"""
        result = self.controller.process_step(
            self.current_session_id,
            PromptCollectionStep.LEARNING_STYLE,
            {"learning_style": style}
        )
        return self.update_interface_for_step(result["next_step"])
    
    def handle_goals(self, short_term: str, long_term: str) -> Dict:
        """Process goals input"""
        goals_data = {
            "short_term": short_term,
            "long_term": long_term
        }
        result = self.controller.process_step(
            self.current_session_id,
            PromptCollectionStep.GOALS,
            goals_data
        )
        return self.update_interface_for_step(result["next_step"])
    
    def handle_interests(self, interests: list, other: str) -> Dict:
        """Process interests input"""
        interests_data = {
            "selected": interests,
            "other": other
        }
        result = self.controller.process_step(
            self.current_session_id,
            PromptCollectionStep.INTERESTS,
            interests_data
        )
        return self.update_interface_for_step(result["next_step"])
    
    def update_interface_for_step(self, step: PromptCollectionStep) -> Dict:
        """Update UI components based on current step"""
        progress = self.controller.get_session_progress(self.current_session_id)
        self.progress_bar.update(progress["progress_percentage"])
        
        visibility_map = {
            self.learning_style_form: step == PromptCollectionStep.LEARNING_STYLE,
            self.goals_form: step == PromptCollectionStep.GOALS,
            self.interests_form: step == PromptCollectionStep.INTERESTS,
            self.review_form: step == PromptCollectionStep.REVIEW
        }
        
        for component, visible in visibility_map.items():
            component.update(visible=visible)
            
        if step == PromptCollectionStep.REVIEW:
            self.update_review_form()
            
        return {"message": f"Proceeding to {step} step"}
    
    def update_review_form(self):
        """Update the review form with collected preferences"""
        session = self.controller.get_session(self.current_session_id)
        preferences = session.collected_preferences
        
        summary_text = f"""
        ### Your Learning Profile
        
        **Learning Style**: {preferences.get('learning_style', 'Not specified')}
        
        **Goals**:
        - Short-term: {preferences.get('goals', {}).get('short_term', 'Not specified')}
        - Long-term: {preferences.get('goals', {}).get('long_term', 'Not specified')}
        
        **Interests**: {', '.join(preferences.get('interests', {}).get('selected', ['None']))}
        """
        
        self.summary.update(value=summary_text)
        prompt = self.controller.generate_final_prompt(self.current_session_id)
        self.prompt_preview.update(value=prompt)
    
    def reset_session(self):
        """Reset the current session and start over"""
        self.controller.reset_session(self.current_session_id)
        return self.update_interface_for_step(PromptCollectionStep.INIT)
    
    def complete_session(self):
        """Complete the meta prompt session"""
        session = self.controller.get_session(self.current_session_id)
        if session.generated_prompt:
            return {"message": "Session completed successfully!"}
        return {"message": "Error: Could not complete session"}