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
        submissions_data = []
        
        for submission in submissions:
            submissions_data.append({
                'submissionId': submission.id,
                'mcqId': submission.mcq_id,
                'username': submission.username,
                'selectedAnswer': submission.selected_answer,
                'correctAnswer': submission.correct_answer,
                'isCorrect': submission.is_correct,
                'submittedAt': submission.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'success': True,
            'data': submissions_data,
            'count': len(submissions_data)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500 