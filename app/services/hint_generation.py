import os
from openai import OpenAI, AsyncOpenAI
from typing import Dict, Union, Optional, List
from config import Config
from dotenv import load_dotenv
from flask import current_app

# Load environment variables from .env file
load_dotenv()

class HintGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the HintGenerator with an optional API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"

    def generate_hint(self, question: str, current_code: str, template_code: Optional[str] = None) -> Optional[str]:
        """
        Generate a hint for a Python coding question
        
        Args:
            question (str): The programming question or task description
            current_code (str): The student's current code attempt
            template_code (str, optional): Template or starter code if any
            
        Returns:
            str: Generated hint or None if generation fails
        """
        try:
            prompt = f"""
            Programming Question: {question}

            {"Template Code:" + template_code if template_code else ""}

            Student's Current Code:
            {current_code}

            Analyze the code and provide a helpful hint that:
            1. Identifies the main issue or area of improvement
            2. Guides without giving away the complete solution
            3. Uses pedagogical best practices
            4. Focuses on Python concepts and best practices

            Keep the hint concise (2-3 sentences) and constructive.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful Python programming tutor who only gives hints and not full answers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
            
        except Exception as e:
            current_app.logger.error(f"Error generating hint: {str(e)}")
            return None

    def validate_inputs(self, question: str, current_code: str) -> Dict[str, Union[bool, str]]:
        """Validate the input parameters"""
        if not current_code or not question:
            return {
                "success": False,
                "error": "Current code and question are required"
            }
        
        if len(current_code) > 10000:
            return {
                "success": False,
                "error": "Code length exceeds maximum limit of 10000 characters"
            }
            
        if len(question) > 1000:
            return {
                "success": False,
                "error": "Question length exceeds maximum limit of 1000 characters"
            }
            
        return {"success": True} 