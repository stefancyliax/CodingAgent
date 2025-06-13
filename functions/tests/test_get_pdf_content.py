import unittest
import unittest
import unittest
import os
import sys

# Add the parent directory of 'functions' to the Python path
# to allow direct import of 'functions.get_pdf_content'
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)
# sys.path.insert(0, os.path.dirname(parent_dir)) # To find the 'calculator' dir from root

from functions.get_pdf_content import get_pdf_content

# Define the working directory relative to the root of the project
# Assuming this test file is in functions/tests/ and working_directory is ./calculator
WORKING_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "calculator"))

# Create a dummy text file for testing non-PDF case
if not os.path.exists(os.path.join(WORKING_DIRECTORY, "dummy_text_file.txt")):
    with open(os.path.join(WORKING_DIRECTORY, "dummy_text_file.txt"), "w") as f:
        f.write("This is a dummy text file.")

class TestGetPdfContent(unittest.TestCase):

    def test_extract_text_from_pdf(self):
        pdf_path = "test_document.pdf" # Relative to WORKING_DIRECTORY
        expected_text = "This is a test PDF document for testing the get_pdf_content function."
        actual_text = get_pdf_content(WORKING_DIRECTORY, pdf_path)
        self.assertEqual(actual_text.strip(), expected_text)

    def test_file_not_found(self):
        pdf_path = "non_existent_document.pdf"
        expected_error = f'Error: File not found or is not a regular file: "{pdf_path}"'
        actual_error = get_pdf_content(WORKING_DIRECTORY, pdf_path)
        self.assertEqual(actual_error, expected_error)

    def test_not_a_pdf_file(self):
        # Using an existing text file, assuming one exists in the calculator directory
        # Or create one for the test. Let's use the dummy_text_file.txt
        txt_file_path = "dummy_text_file.txt"
        expected_error = f'Error: File "{txt_file_path}" is not a PDF file.'
        actual_error = get_pdf_content(WORKING_DIRECTORY, txt_file_path)
        self.assertEqual(actual_error, expected_error)

    def test_path_outside_working_directory(self):
        # Attempt to access a file outside the working directory.
        # This path will vary based on the test execution environment,
        # so constructing a reliable outside path is tricky.
        # Let's try to go up one level from the project root (where calculator is)
        # This assumes 'calculator' is not the filesystem root.
        # The exact path might need adjustment depending on test runner's CWD.
        # For now, this demonstrates the intent.
        # A more robust way would be to mock os.path.abspath

        # ../../some_other_file.pdf from 'calculator' directory
        # This will resolve to <project_root>/../some_other_file.pdf
        # This will be outside the working directory which is <project_root>/calculator
        invalid_path = "../../outside_file.pdf"

        # Create a dummy file there for the check to pass the isfile check if it were allowed
        # For safety, this part of the test might be better mocked or made conditional
        # For now, we'll just test the path check itself.
        # The function should prevent access before any actual file operations.

        expected_error_fragment = 'Error: Cannot read "'
        expected_error_fragment_end = '" as it is outside the permitted working directory'
        actual_error = get_pdf_content(WORKING_DIRECTORY, invalid_path)
        self.assertTrue(actual_error.startswith(expected_error_fragment))
        self.assertTrue(actual_error.endswith(expected_error_fragment_end))


if __name__ == '__main__':
    unittest.main()
