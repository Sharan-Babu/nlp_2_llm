from typing import AnyStr, Any
from gentopia.tools.basetool import *
import re
from collections import Counter

class TextAnalyzerArgs(BaseModel):
    text: str = Field(..., description="Text to analyze.")
    analysis_type: str = Field(..., description="Type of analysis to perform: 'word_count', 'char_count', 'sentence_count', 'avg_word_length', 'most_common_words', or 'all'.")

class TextAnalyzer(BaseTool):
    """Tool that performs various text analysis tasks"""

    name = "text_analyzer"
    description = (
        "Analyzes the input text and provides various statistics. "
        "It can count words, characters, sentences, calculate average word length, "
        "and find most common words. "
        "Input should be a text string and the type of analysis to perform."
    )
    args_schema: Optional[Type[BaseModel]] = TextAnalyzerArgs

    def _run(self, text: AnyStr, analysis_type: AnyStr) -> AnyStr:
        text = text.strip()
        
        def word_count(text):
            return len(text.split())

        def char_count(text):
            return len(text)

        def sentence_count(text):
            return len(re.findall(r'\w+[.!?]', text))

        def avg_word_length(text):
            words = text.split()
            if not words:
                return 0
            return sum(len(word) for word in words) / len(words)

        def most_common_words(text, n=5):
            words = re.findall(r'\w+', text.lower())
            return Counter(words).most_common(n)

        analysis_functions = {
            'word_count': word_count,
            'char_count': char_count,
            'sentence_count': sentence_count,
            'avg_word_length': avg_word_length,
            'most_common_words': most_common_words
        }

        if analysis_type == 'all':
            results = {}
            for name, func in analysis_functions.items():
                results[name] = func(text)
            return "\n".join(f"{name}: {value}" for name, value in results.items())
        elif analysis_type in analysis_functions:
            result = analysis_functions[analysis_type](text)
            return f"{analysis_type}: {result}"
        else:
            return f"Invalid analysis type. Choose from: {', '.join(analysis_functions.keys())}, or 'all'."

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    analyzer = TextAnalyzer()
    sample_text = "This is a sample text. It contains multiple sentences. The purpose is to demonstrate the text analyzer tool."
    print(analyzer._run(sample_text, "all"))
    print(analyzer._run(sample_text, "word_count"))
    print(analyzer._run(sample_text, "most_common_words"))