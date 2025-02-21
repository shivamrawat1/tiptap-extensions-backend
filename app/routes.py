from flask import Blueprint, request, jsonify
from app.models.mcq_submission import MCQSubmission
from app import db
from flask_cors import CORS
from app.services.code_executor import execute_code
from app.services.hint_generation import HintGenerator
from flask import current_app

# Create blueprint
api_bp = Blueprint('api', __name__)
CORS(api_bp)

hint_generator = HintGenerator()

@api_bp.route('/hint/generate', methods=['POST', 'OPTIONS'])  # Changed from mcq_bp to api_bp and fixed route path
def generate_hint():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({'success': True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    data = request.get_json()
    
    # Validate required fields
    required_fields = ['question', 'currentCode']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400

    # Validate inputs
    validation_result = hint_generator.validate_inputs(
        data['question'],
        data['currentCode']
    )
    
    if not validation_result['success']:
        return jsonify(validation_result), 400

    hint = hint_generator.generate_hint(
        question=data['question'],
        current_code=data['currentCode'],
        template_code=data.get('templateCode')  # Optional template code
    )

    if hint is None:
        return jsonify({
            'success': False,
            'message': 'Failed to generate hint'
        }), 500

    return jsonify({
        'success': True,
        'hint': hint
    })

@api_bp.route('/mcq/submit', methods=['POST'])
def submit_mcq():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['mcqId', 'selectedAnswer', 'correctAnswer', 'username']
        for field in required_fields:
            if field not in data or not data[field]:  # Just add this check for empty values
                return jsonify({
                    'success': False,
                    'message': f'Missing or empty required field: {field}'
                }), 400

        # Create submission
        submission = MCQSubmission(
            mcq_id=data['mcqId'],
            username=data['username'],
            selected_answer=data['selectedAnswer'],
            correct_answer=data['correctAnswer']
        )

        try:
            # Save to database
            db.session.add(submission)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Database error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Failed to save submission'
            }), 500

        return jsonify({
            'success': True,
            'message': 'Submission recorded successfully',
            'submissionId': submission.id
        }), 201

    except Exception as e:
        current_app.logger.error(f"Server error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Server error occurred'
        }), 500

@api_bp.route('/mcq/submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = MCQSubmission.query.all()
        return jsonify({
            'success': True,
            'data': [submission.to_dict() for submission in submissions],
            'count': len(submissions)
        }), 200
    except Exception as e:
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to fetch submissions'
        }), 500

@api_bp.route('/python/execute', methods=['POST', 'OPTIONS'])
def execute_python():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                'success': False,
                'error': 'No code provided'
            }), 400

        if not isinstance(data['code'], str):
            return jsonify({
                'success': False,
                'error': 'Code must be a string'
            }), 400

        code = data['code'].strip()
        if not code:
            return jsonify({
                'success': False,
                'error': 'Code cannot be empty'
            }), 400

        result = execute_code(code)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500 