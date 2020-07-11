import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        """Test for get_all_categories
        Tests for the status code, if success is true,
        if categories is returned and the length of
        the returned categories
        """

        # make request and process response
        response = self.client().get('/categories')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)


    def test_error_for_out_of_bound_page(self):
        response = self.client().get('/questions?page=8998')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_question_id_not_exist(self):
        """Tests deletion of question id that doesn't exist
        This tests the error message returned a valid id that
        doesn't exist is used.
        """
        # this tests an id that doesn't exist
        response = self.client().delete('/questions/1211256')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_question_with_invalid_id(self):
        """Tests deletion of question with invalid id"""
        # this tests an invalid id
        response = self.client().delete('/questions/sadsa2112kjsds6')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_questions(self):
        """Test for creating question."""

        # mock data to use as payload for post request
        mock_data = {
            'question': 'This is a mock question',
            'answer': 'this is a mock answer',
            'difficulty': 1,
            'category': 1,
        }

        # make request and process response
        response = self.client().post('/questions', json=mock_data)
        data = json.loads(response.data)

        # asserions to ensure successful request
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')

    def test_create_question_with_empty_data(self):
        """Test for ensuring data with empty fields are not processed."""
        request_data = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': 1,
        }

        # make request and process response
        response = self.client().post('/questions', json=request_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_search_questions(self):
        """Test for searching for a question."""

        request_data = {
            'searchTerm': 'largest lake in Africa',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_empty_search_term_response(self):
        """Test for empty search term."""

        request_data = {
            'searchTerm': '',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_search_term_not_found(self):
        """Test for search term not found."""

        request_data = {
            'searchTerm': 'xc',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions_by_category(self):
        """Test for getting questions by category."""

        # make a request for the Sports category with id of 6
        response = self.client().get('/categories/6/questions')
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Sports')

    def test_invalid_category_id(self):
        """Test for invalid category id"""

        # request with invalid category id 1987
        response = self.client().get('/categories/1987/questions')
        data = json.loads(response.data)

        # Assertions to ensure 422 error is returned
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
