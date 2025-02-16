# -*- coding: utf-8 -*-
from typing import Dict, List, Optional
import json

from .base import BaseAIAgent
from models.meta_prompt_session import MetaPromptSession
from models.user import UserModel


class MetaPromptAgent(BaseAIAgent):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.collection_prompts = {
            "learning_style": "Based on the user's background as a {occupation} aged {age}, what would be their most effective learning style?",
            "goals": "What specific learning goals would be most beneficial for a {occupation} aged {age} named {name}?",
            "interests": "What topics or areas might interest a {occupation} like {name} who is {age} years old?",
        }

    def analyze_user_preferences(self, user: UserModel) -> Dict:
        """Analyze user information to determine optimal learning preferences"""
        messages = [
            {
                "role": "system",
                "content": "You are an AI learning specialist analyzing user data to determine optimal learning preferences."
            },
            {
                "role": "user",
                "content": f"Analyze the following user: Name: {user.name}, Age: {user.age}, Occupation: {user.occupation}"
            }
        ]
        analysis = self.generate_response(messages)
        return json.loads(analysis)

    def collect_preferences(self, user: UserModel, preference_type: str) -> str:
        """Collect specific user preferences through targeted prompting"""
        prompt_template = self.collection_prompts.get(preference_type)
        if not prompt_template:
            raise ValueError(f"Unknown preference type: {preference_type}")
        
        prompt = prompt_template.format(
            name=user.name,
            age=user.age,
            occupation=user.occupation
        )
        
        messages = [
            {"role": "system", "content": "You are a learning preference analyst."},
            {"role": "user", "content": prompt}
        ]
        return self.generate_response(messages)

    def generate_personalized_prompt(self, session: MetaPromptSession) -> str:
        """Generate a personalized learning prompt based on collected preferences"""
        preferences = session.collected_preferences
        user = session.user

        context = {
            "learning_style": preferences.get("learning_style", ""),
            "goals": preferences.get("goals", []),
            "interests": preferences.get("interests", []),
            "user_info": {
                "name": user.name,
                "age": user.age,
                "occupation": user.occupation
            }
        }

        messages = [
            {
                "role": "system",
                "content": "You are an AI specializing in creating personalized learning experiences."
            },
            {
                "role": "user",
                "content": f"Create a personalized learning prompt for a user with the following context: {json.dumps(context)}"
            }
        ]
        return self.generate_response(messages)

    def analyze_learning_goals(self, goals: List[str]) -> Dict:
        """Analyze and structure learning goals for better personalization"""
        messages = [
            {
                "role": "system",
                "content": "You are an AI learning goals analyst."
            },
            {
                "role": "user",
                "content": f"Analyze and structure these learning goals: {goals}"
            }
        ]
        analysis = self.generate_response(messages)
        return json.loads(analysis)

    def suggest_learning_path(self, user: UserModel, session: MetaPromptSession) -> Dict:
        """Suggest a personalized learning path based on user preferences and goals"""
        preferences = session.collected_preferences
        messages = [
            {
                "role": "system",
                "content": "You are an AI learning path advisor."
            },
            {
                "role": "user",
                "content": f"Create a learning path for user with preferences: {json.dumps(preferences)}"
            }
        ]
        path_suggestion = self.generate_response(messages)
        return json.loads(path_suggestion)

    def adapt_prompt_style(self, prompt: str, user_preferences: Dict) -> str:
        """Adapt the prompt style based on user preferences"""
        messages = [
            {
                "role": "system",
                "content": "You are an AI specializing in communication style adaptation."
            },
            {
                "role": "user",
                "content": f"Adapt this prompt: '{prompt}' to match preferences: {json.dumps(user_preferences)}"
            }
        ]
        return self.generate_response(messages)