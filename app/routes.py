from flask import Blueprint, request, jsonify
from app.models.mcq_submission import MCQSubmission
from app import db

mcq_bp = Blueprint('mcq', __name__)

@mcq_bp.route('/mcq/submit', methods=['POST'])
def submit_mcq():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['mcqId', 'selectedAnswer', 'correctAnswer', 'username']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
            if not isinstance(data[field], str):
                return jsonify({
                    'success': False,
                    'message': f'Invalid data type for field: {field}'
                }), 400

        # Create submission
        submission = MCQSubmission(
            mcq_id=data['mcqId'],
            username=data['username'],
            selected_answer=data['selectedAnswer'],
            correct_answer=data['correctAnswer']
        )

        # Save to database
        db.session.add(submission)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Submission recorded successfully',
            'submissionId': submission.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@mcq_bp.route('/mcq/submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = MCQSubmission.query.all()
        return jsonify({
            'success': True,
            'data': [{
                'id': sub.id,
                'mcqId': sub.mcq_id,
                'username': sub.username,
                'selectedAnswer': sub.selected_answer,
                'correctAnswer': sub.correct_answer,
                'isCorrect': sub.is_correct,
                'submittedAt': sub.submitted_at.isoformat()
            } for sub in submissions],
            'count': len(submissions)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500 