"""Main entry point for the Vortex of Enlightenment game."""

from core.engine import CoreEngine
from core.ui import TerminalUI
from core.intro import IntroSequence
from core.questionnaire import QuestionnaireEngine

def main():
    """Main entry point for the game."""
    try:
        # Run introduction sequence
        intro = IntroSequence()
        profile = intro.run_sequence()
        
        if not profile:
            return
            
        # Run the questionnaire
        questionnaire = QuestionnaireEngine()
        profile_impacts = questionnaire.run_questionnaire()
        
        # Initialize core components with profile data
        engine = CoreEngine()
        ui = TerminalUI()
        
        # TODO: Update profile with questionnaire results
        
        # Start the game engine
        engine.start()
        
        # Main game loop
        while engine.state.is_running:
            # Get and process user input
            user_input = ui.get_input()
            result = ui.process_input(user_input)
            
            # Display the result
            if result:
                ui.display(result)
                
    except KeyboardInterrupt:
        print("\nThank you for playing Vortex of Enlightenment!")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("The game has been terminated.")

if __name__ == "__main__":
    main() 