import unittest
from vortex.src.core.user_profiling.questionnaire import VoightKampffQuestionnaire, Question
from vortex.src.core.user_profiling.profile_matrix import ProfileDimension

class TestVoightKampffQuestionnaire(unittest.TestCase):
    def setUp(self):
        self.questionnaire = VoightKampffQuestionnaire()

    def test_questionnaire_initialization(self):
        """Test that questionnaire is properly initialized with questions."""
        self.assertGreater(len(self.questionnaire.questions), 0)
        
        # Test first question structure
        first_question = self.questionnaire.questions[0]
        self.assertIsInstance(first_question, Question)
        self.assertTrue(hasattr(first_question, 'id'))
        self.assertTrue(hasattr(first_question, 'text'))
        self.assertTrue(hasattr(first_question, 'options'))
        self.assertTrue(hasattr(first_question, 'dimension_impacts'))
        self.assertTrue(hasattr(first_question, 'human_detection_weight'))

    def test_get_question(self):
        """Test retrieving questions by index."""
        # Test valid index
        question = self.questionnaire.get_question(0)
        self.assertIsNotNone(question)
        self.assertIsInstance(question, Question)

        # Test invalid indices
        self.assertIsNone(self.questionnaire.get_question(-1))
        self.assertIsNone(self.questionnaire.get_question(1000))

    def test_analyze_response(self):
        """Test response analysis functionality."""
        question = self.questionnaire.get_question(0)
        
        # Test valid response
        impacts = self.questionnaire.analyze_response(question, 0)
        self.assertIsInstance(impacts, dict)
        self.assertIn('human_probability', impacts)
        
        # Test impact values are within valid range
        for value in impacts.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

        # Test invalid option index
        with self.assertRaises(ValueError):
            self.questionnaire.analyze_response(question, -1)
        with self.assertRaises(ValueError):
            self.questionnaire.analyze_response(question, len(question.options))

    def test_question_structure(self):
        """Test that all questions have valid structure and content."""
        for question in self.questionnaire.questions:
            # Check basic attributes
            self.assertTrue(isinstance(question.id, str))
            self.assertTrue(isinstance(question.text, str))
            self.assertTrue(isinstance(question.options, list))
            self.assertTrue(isinstance(question.dimension_impacts, dict))
            self.assertTrue(isinstance(question.human_detection_weight, float))
            
            # Check options
            self.assertGreater(len(question.options), 0)
            for option in question.options:
                self.assertTrue(isinstance(option, str))
            
            # Check dimension impacts
            for dimension, impact in question.dimension_impacts.items():
                self.assertIsInstance(dimension, ProfileDimension)
                self.assertGreaterEqual(impact, 0.0)
                self.assertLessEqual(impact, 1.0)
            
            # Check human detection weight
            self.assertGreaterEqual(question.human_detection_weight, 0.0)
            self.assertLessEqual(question.human_detection_weight, 1.0)

if __name__ == '__main__':
    unittest.main() 