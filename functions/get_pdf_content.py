import os
import PyPDF2
from google.genai import types

MAX_CHARS = 10000

def get_pdf_content(working_directory, file_path):
    """
    Extracts text content from a PDF file, constrained to the working directory.

    Args:
        working_directory: The working directory.
        file_path: The path to the PDF file, relative to the working directory.

    Returns:
        The extracted text content of the PDF, or an error message.
    """
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_dir_abs, file_path))

    if not target_file.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    if not file_path.lower().endswith(".pdf"):
        return f'Error: File "{file_path}" is not a PDF file.'

    try:
        with open(target_file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                extracted_page_text = page.extract_text()
                if extracted_page_text: # Ensure text was extracted
                    text += extracted_page_text
                if len(text) > MAX_CHARS:
                    text = text[:MAX_CHARS]
                    break
            return text
    except Exception as e:
        return f"Error: could not read PDF file: {e}"

schema_get_pdf_content = types.FunctionDeclaration(
    name="get_pdf_content",
    description="Extracts text content from a PDF file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the PDF file, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)
