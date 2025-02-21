import pytest
from datetime import datetime
from app import create_app, db
from app.models.mcq_submission import MCQSubmission


def test_submit_mcq_endpoint(client, ctx):
    """Test the MCQ submission endpoint"""
    test_data = {
        "mcqId": "test-mcq-1",
        "username": "testuser",
        "selectedAnswer": "A",
        "correctAnswer": "B"
    }
    
    response = client.post('/api/mcq/submit', json=test_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['success']
    assert 'submissionId' in data


def test_get_submissions_endpoint(client, ctx):
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

    response = client.get('/api/mcq/submissions')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success']
    assert len(data['data']) == 1
    assert data['count'] == 1
    
    submission_data = data['data'][0]
    assert submission_data['mcqId'] == "test-mcq-1"
    assert submission_data['username'] == "testuser"
    assert submission_data['selectedAnswer'] == "A"
    assert submission_data['correctAnswer'] == "B"
    assert not submission_data['isCorrect'] 