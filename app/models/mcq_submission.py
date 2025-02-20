from datetime import datetime
import uuid
from app import db

class MCQSubmission(db.Model):
    __tablename__ = 'mcq_submissions'
    
    id = db.Column(db.String(36), primary_key=True)
    mcq_id = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    selected_answer = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, mcq_id, username, selected_answer, correct_answer):
        self.id = str(uuid.uuid4())
        self.mcq_id = mcq_id
        self.username = username
        self.selected_answer = selected_answer
        self.correct_answer = correct_answer
        self.is_correct = selected_answer == correct_answer 