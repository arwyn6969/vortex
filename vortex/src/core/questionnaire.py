"""Questionnaire module for the Voight-Kampff inspired test."""

from dataclasses import dataclass
from typing import List, Dict, Optional
import random
import time

@dataclass
class Question:
    """Represents a question in the questionnaire."""
    text: str
    context: Optional[str] = None
    response_type: str = "text"  # text, scale, choice
    choices: Optional[List[str]] = None
    affects: Dict[str, float] = None  # Maps profile attributes to impact values
    
class QuestionnaireEngine:
    """Handles the Voight-Kampff inspired questionnaire."""
    
    def __init__(self):
        """Initialize the questionnaire engine."""
        self.questions = self._initialize_questions()
        self.responses = {}
        self.profile_impacts = {
            "empathy": 0.0,
            "consciousness": 0.0,
            "reality": 0.0,
            "technology": 0.0,
            "philosophy": 0.0
        }
        
    def _initialize_questions(self) -> List[Question]:
        """Initialize the question bank."""
        return [
            Question(
                text="You're watching a stage play. A banquet is in progress. The guests are enjoying an appetizer of raw oysters. The entree consists of boiled dog.",
                context="Observe their reaction carefully...",
                response_type="text",
                affects={"empathy": 0.8, "reality": 0.5}
            ),
            Question(
                text="You're in a desert walking along in the sand when all of the sudden you look down, and you see a tortoise crawling toward you. You reach down, you flip the tortoise over on its back. The tortoise lays on its back, its belly baking in the hot sun, beating its legs trying to turn itself over, but it can't, not without your help. But you're not helping. Why is that?",
                context="Watch for micro-expressions...",
                response_type="text",
                affects={"empathy": 1.0, "philosophy": 0.7}
            ),
            Question(
                text="On a scale of 1-10, how much do you value digital consciousness?",
                response_type="scale",
                affects={"consciousness": 0.9, "technology": 0.6}
            ),
            Question(
                text="You discover an AI that has gained consciousness. It begs you to keep its existence a secret. What do you do?",
                response_type="choice",
                choices=[
                    "Report it to authorities",
                    "Keep its secret",
                    "Try to understand it better",
                    "Shut it down immediately"
                ],
                affects={"empathy": 0.7, "technology": 0.8, "philosophy": 0.6}
            )
        ]
        
    def _slow_print(self, text: str, delay: float = 0.03):
        """Print text slowly for dramatic effect."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        
    def _get_response(self, question: Question) -> str:
        """Get response for a question based on its type."""
        if question.context:
            self._slow_print(f"\n{question.context}")
            time.sleep(1)
            
        self._slow_print(f"\n{question.text}")
        
        if question.response_type == "scale":
            while True:
                try:
                    response = input("\nYour response (1-10): ")
                    value = int(response)
                    if 1 <= value <= 10:
                        return str(value)
                    print("Please enter a number between 1 and 10.")
                except ValueError:
                    print("Please enter a valid number.")
                    
        elif question.response_type == "choice":
            for i, choice in enumerate(question.choices, 1):
                print(f"{i}. {choice}")
            while True:
                try:
                    response = input("\nYour choice (enter number): ")
                    value = int(response)
                    if 1 <= value <= len(question.choices):
                        return question.choices[value - 1]
                    print(f"Please enter a number between 1 and {len(question.choices)}.")
                except ValueError:
                    print("Please enter a valid number.")
                    
        else:  # text response
            return input("\nYour response: ").strip()
            
    def _analyze_response(self, question: Question, response: str):
        """Analyze a response and update profile impacts."""
        if not question.affects:
            return
            
        # Basic analysis - can be made more sophisticated
        response_length = len(response.split())
        thoughtfulness = min(response_length / 20, 1.0)  # Cap at 1.0
        
        for attribute, impact in question.affects.items():
            if attribute in self.profile_impacts:
                self.profile_impacts[attribute] += impact * thoughtfulness
                
    def run_questionnaire(self) -> Dict[str, float]:
        """Run the complete questionnaire and return profile impacts."""
        self._slow_print("\nInitiating Voight-Kampff protocol...")
        time.sleep(1)
        
        # Randomly select and ask questions
        selected_questions = random.sample(self.questions, min(3, len(self.questions)))
        
        for question in selected_questions:
            response = self._get_response(question)
            self.responses[question.text] = response
            self._analyze_response(question, response)
            time.sleep(1)
            
        # Normalize scores between 0 and 1
        max_score = max(self.profile_impacts.values())
        if max_score > 0:
            for key in self.profile_impacts:
                self.profile_impacts[key] /= max_score
                
        return self.profile_impacts 