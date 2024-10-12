from typing import AnyStr, Any, Optional, Type
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *
import io

class PDFReaderArgs(BaseModel):
    url: str = Field(..., description="The full URL of the PDF to be downloaded and read.")

class PDFReader(BaseTool):
    """Tool that downloads a PDF file from a URL, reads it and returns the text"""

    name = "pdf_reader"
    description = (
        "A PDF Reader that can download a PDF from a URL and extract text from it. "
        "It returns the content of the PDF as a string."
    )
    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs
    maxlen_per_page = 2000

    def _run(self, url: AnyStr) -> AnyStr:
        try:
            # Step 1: Download the PDF file from the provided URL
            response = requests.get(url)
            print(url)
            print(response)
            
            # Check if the request was successful
            if response.status_code != 200:
                return f"Failed to retrieve PDF. HTTP status code: {response.status_code}"
            
            # Step 2: Load the PDF into memory as a file-like object
            pdf_file = BytesIO(response.content)
            reader = PdfReader(pdf_file)

            # Step 3: Extract and accumulate text from each page
            text_list = []
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                
                # Check if the page contains text, then limit the length of the text per page
                if text:
                    text_list.append(f"Page {page_num+1}:\n{text[:self.maxlen_per_page]}\n")
                else:
                    text_list.append(f"Page {page_num+1} contains no extractable text.\n")

            # Step 4: Combine all pages' text and return
            if text_list:
                return "\n".join(text_list)
            else:
                return "The PDF contains no readable text."

        except Exception as ex:
            return f"An error occurred while downloading or reading the PDF: {ex}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    # Example usage
    ans = PDFReader()._run("https://arxiv.org/pdf/2103.00020.pdf")
    print(ans)
