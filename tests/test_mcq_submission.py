import unittest
from datetime import datetime
from app import create_app, db
from app.models.mcq_submission import MCQSubmission

class TestMCQSubmission(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_mcq_submission_creation(self):
        """Test MCQSubmission model creation"""
        submission = MCQSubmission(
            mcq_id="test-mcq-1",
            username="testuser",
            selected_answer="A",
            correct_answer="A"
        )
        
        self.assertEqual(submission.mcq_id, "test-mcq-1")
        self.assertEqual(submission.username, "testuser")
        self.assertEqual(submission.selected_answer, "A")
        self.assertEqual(submission.correct_answer, "A")
        self.assertTrue(submission.is_correct)
        self.assertIsInstance(submission.id, str)
        self.assertTrue(len(submission.id) > 0)

    def test_submit_mcq_endpoint(self):
        """Test the MCQ submission endpoint"""
        test_data = {
            "mcqId": "test-mcq-1",
            "username": "testuser",
            "selectedAnswer": "A",
            "correctAnswer": "B"
        }
        
        response = self.client.post('/api/mcq/submit', json=test_data)
        self.assertEqual(response.status_code, 201)
        
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('submissionId', data)

    def test_submit_mcq_invalid_data(self):
        """Test MCQ submission with invalid data"""
        test_data = {
            "mcqId": "test-mcq-1",
            # Missing username field
            "selectedAnswer": "A",
            "correctAnswer": "B"
        }
        
        response = self.client.post('/api/mcq/submit', json=test_data)
        self.assertEqual(response.status_code, 400)
        
        data = response.get_json()
        self.assertFalse(data['success'])
        self.assertIn('Missing required field', data['message'])

    def test_get_submissions_endpoint(self):
        """Test getting all submissions"""
        # First ensure the database is empty
        MCQSubmission.query.delete()
        db.session.commit()
        
        # Create a test submission
        submission = MCQSubmission(
            mcq_id="test-mcq-1",
            username="testuser",
            selected_answer="A",
            correct_answer="B"
        )
        db.session.add(submission)
        db.session.commit()

        response = self.client.get('/api/mcq/submissions')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['count'], 1)
        
        submission_data = data['data'][0]
        self.assertEqual(submission_data['mcqId'], "test-mcq-1")
        self.assertEqual(submission_data['username'], "testuser")
        self.assertEqual(submission_data['selectedAnswer'], "A")
        self.assertEqual(submission_data['correctAnswer'], "B")
        self.assertFalse(submission_data['isCorrect'])

if __name__ == '__main__':
    unittest.main() 