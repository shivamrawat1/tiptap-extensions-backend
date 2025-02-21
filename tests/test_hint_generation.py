import pytest
from app.services.hint_generation import HintGenerator

def test_hint_generation_endpoint(client, ctx):
    """Test the hint generation endpoint"""
    test_data = {
        "question": "Write a function that calculates the factorial of a number",
        "currentCode": """def factorial(n):
    if n == 0:
    return 1""",
        "templateCode": """def factorial(n):
    # Your code here
    pass"""
    }
    
    response = client.post('/api/hint/generate', json=test_data)
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['success']
    assert 'hint' in data
    assert isinstance(data['hint'], str)
    assert len(data['hint']) > 0

def test_hint_generation_invalid_data(client, ctx):
    """Test hint generation with invalid data"""
    test_data = {
        "question": "Write a function that calculates the factorial of a number",
        # Missing currentCode field
    }
    
    response = client.post('/api/hint/generate', json=test_data)
    assert response.status_code == 400
    
    data = response.get_json()
    assert not data['success']
    assert 'Missing required field' in data['message']

def test_hint_generation_long_code(client, ctx):
    """Test hint generation with code exceeding length limit"""
    test_data = {
        "question": "Write a function",
        "currentCode": "print('hello')" * 2000  # Will exceed 10000 characters
    }
    
    response = client.post('/api/hint/generate', json=test_data)
    assert response.status_code == 400
    
    data = response.get_json()
    assert not data['success']
    assert 'exceeds maximum limit' in data['error']

def test_hint_generation_service(ctx):
    """Test the HintGenerator service directly"""
    hint_generator = HintGenerator()
    
    question = "Write a function that calculates the factorial of a number"
    current_code = """def factorial(n):
    if n == 0:
    return 1"""
    
    hint = hint_generator.generate_hint(
        question=question,
        current_code=current_code
    )
    
    assert hint is not None
    assert isinstance(hint, str)
    assert len(hint) > 0

def test_input_validation(ctx):
    """Test input validation in HintGenerator"""
    hint_generator = HintGenerator()
    
    # Test with empty inputs
    result = hint_generator.validate_inputs("", "")
    assert not result['success']
    assert 'required' in result['error']
    
    # Test with valid inputs
    result = hint_generator.validate_inputs("Write a function", "def test(): pass")
    assert result['success']
    
    # Test with long question
    long_question = "Write a function" * 200  # Will exceed 1000 characters
    result = hint_generator.validate_inputs(long_question, "def test(): pass")
    assert not result['success']
    assert 'exceeds maximum limit' in result['error'] 