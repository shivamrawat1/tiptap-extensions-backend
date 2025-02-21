from datetime import datetime
import uuid
from app import db

class MCQSubmission(db.Model):
    __tablename__ = 'mcq_submissions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mcq_id = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    selected_answer = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_correct(self):
        return self.selected_answer == self.correct_answer

    def to_dict(self):
        return {
            'id': self.id,
            'mcqId': self.mcq_id,
            'username': self.username,
            'selectedAnswer': self.selected_answer,
            'correctAnswer': self.correct_answer,
            'isCorrect': self.is_correct,
            'submittedAt': self.submitted_at.isoformat()
        }

    def __init__(self, mcq_id, username, selected_answer, correct_answer):
        self.mcq_id = mcq_id
        self.username = username
        self.selected_answer = selected_answer
        self.correct_answer = correct_answer 