from typing import AnyStr
from pypdf import PdfReader
from gentopia.tools.basetool import *
import requests
import io

class PDFReadingArgs(BaseModel):
    file_path: str = Field(..., description="Path to the PDF file")


class PDFReading(BaseTool):
    """Tool that reads text content from a PDF file."""

    name = "pdf_reading"
    description = "A tool for extracting text content from a PDF file."

    args_schema: Optional[Type[BaseModel]] = PDFReadingArgs

    def _run(self, file_path: AnyStr) -> str:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
        response = requests.get(file_path, headers)
        pdf_file = io.BytesIO(response.content)

        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ""
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

        return text

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    # Example usage
    file_path = "example.pdf"  # Replace with the actual path to the PDF file
    ans = PDFReading()._run(file_path)
    print(ans)
