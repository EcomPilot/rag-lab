# code source: https://gist.github.com/hanxiao/3f60354cf6dc5ac698bc9154163b4e6a
# link: https://jina.ai/tokenizer/

import regex

MAX_HEADING_LENGTH = 7
MAX_HEADING_CONTENT_LENGTH = 200
MAX_HEADING_UNDERLINE_LENGTH = 200
MAX_HTML_HEADING_ATTRIBUTES_LENGTH = 100
MAX_LIST_ITEM_LENGTH = 200
MAX_NESTED_LIST_ITEMS = 6
MAX_LIST_INDENT_SPACES = 7
MAX_BLOCKQUOTE_LINE_LENGTH = 200
MAX_BLOCKQUOTE_LINES = 15
MAX_CODE_BLOCK_LENGTH = 1500
MAX_CODE_LANGUAGE_LENGTH = 20
MAX_INDENTED_CODE_LINES = 20
MAX_TABLE_CELL_LENGTH = 200
MAX_TABLE_ROWS = 20
MAX_HTML_TABLE_LENGTH = 2000
MIN_HORIZONTAL_RULE_LENGTH = 3
MAX_SENTENCE_LENGTH = 400
MAX_QUOTED_TEXT_LENGTH = 300
MAX_PARENTHETICAL_CONTENT_LENGTH = 200
MAX_NESTED_PARENTHESES = 5
MAX_MATH_INLINE_LENGTH = 100
MAX_MATH_BLOCK_LENGTH = 500
MAX_PARAGRAPH_LENGTH = 1000
MAX_STANDALONE_LINE_LENGTH = 800
MAX_HTML_TAG_ATTRIBUTES_LENGTH = 100
MAX_HTML_TAG_CONTENT_LENGTH = 1000
LOOKAHEAD_RANGE = 100;  # Number of characters to look ahead for a sentence boundary


def chuncking_executor(text:str, max_chunk_size:int=500, remove_line_breaks:bool=False):
    """
    Splits the input text into chunks of a specified maximum size.

    **Parameters:**
    - text (str): The input text to be chunked.
    - max_chunk_size (int): The maximum size of each chunk. Default is 1000.
    - remove_line_breaks (bool): If True, removes all line breaks from the input text before chunking. Default is False.

    **Returns:**
    - list: A list of non-empty chunks.
    """
    if remove_line_breaks: text = text.replace("\n", "")
    MAX_SENTENCE_LENGTH = max_chunk_size
    pattern = regex.compile(
        # 1. Headings (Setext-style, Markdown, and HTML-style, with length constraints)
        rf"(?:^"
        rf"(?:^(?:[#*=-]{{1,{MAX_HEADING_LENGTH}}}"
        rf"|\w[^\r\n]{{0,{MAX_HEADING_CONTENT_LENGTH}}}\r?\n[-=]{{2,{MAX_HEADING_UNDERLINE_LENGTH}}}"
        rf"|<h[1-6][^>]{{0,{MAX_HTML_HEADING_ATTRIBUTES_LENGTH}}}>[^\r\n]{{1,{MAX_HEADING_CONTENT_LENGTH}}}"
        rf")"
        rf"[^\r\n]{{1,{MAX_HEADING_CONTENT_LENGTH}}})"
        rf"(?:</h[1-6]>)?"
        rf"(?:\r?\n|$)"
        rf")"
        rf"|"
        rf"(?:\[[0-9]+\][^\r\n]{{1,{MAX_STANDALONE_LINE_LENGTH}}})"

        rf"|"

        # 2. List items (bulleted, numbered, lettered, or task lists, including nested, up to three levels, with length constraints)
        rf"(?:(?:^|\r?\n)[ \t]{{0,3}}(?:[-*+•]|\d{{1,3}}\.\w\.|\[[ xX]\])[ \t]+"
        rf"(?:(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))"
        rf"|(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b(?=[\r\n]|$))"
        rf"|(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b(?=[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])"
        rf"(?:.{{1,{LOOKAHEAD_RANGE}}}(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))?))"

        rf"|"

        rf"(?:(?:\r?\n[ \t]{{2,5}}(?:[-*+•]|\d{{1,3}}\.\w\.|\[[ xX]\])[ \t]+"
        rf"(?:(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b"
        rf"(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))"
        rf"|(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b(?=[\r\n]|$))"
        rf"|(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b(?=[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])"
        rf"(?:.{{1,{LOOKAHEAD_RANGE}}}(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))?)))"
        rf"{{0,{MAX_NESTED_LIST_ITEMS}}}"

        rf"|"

        rf"(?:\r?\n[ \t]{{4,{MAX_LIST_INDENT_SPACES}}}(?:[-*+•]|\d{{1,3}}\.\w\.|\[[ xX]\])[ \t]+"
        rf"(?:(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b"
        rf"(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))"
        rf"|(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b(?=[\r\n]|$))"
        rf"|(?:\b[^\r\n]{{1,{MAX_LIST_ITEM_LENGTH}}}\b(?=[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])"
        rf"(?:.{{1,{LOOKAHEAD_RANGE}}}(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))?)))"
        rf"{{0,{MAX_NESTED_LIST_ITEMS}}})?)"

        rf"|"

        # 3. Block quotes (including nested quotes and citations, up to three levels, with length constraints)
        rf"(?:(?:^>(?:>|\s{{2,}}){{0,2}}(?:"
        rf"(?:\b[^\r\n]{{0,{MAX_BLOCKQUOTE_LINE_LENGTH}}}\b(?:[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))"
        rf"|(?:\b[^\r\n]{{0,{MAX_BLOCKQUOTE_LINE_LENGTH}}}\b(?=[\r\n]|$))"
        rf"|(?:\b[^\r\n]{{0,{MAX_BLOCKQUOTE_LINE_LENGTH}}}\b(?=[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])"
        rf"(?:.{{1,{LOOKAHEAD_RANGE}}}(?:[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])"
        rf"(?=\s|$))?))\r?\n?){{1,{MAX_BLOCKQUOTE_LINES}}})"

        rf"|"

        # 4. Code blocks (fenced, indented, or HTML pre/code tags, with length constraints)
        rf"(?:(?:^|\r?\n)(?:\`\`\`|~~~)(?:\w{{0,{MAX_CODE_LANGUAGE_LENGTH}}})?\r?\n[\s\S]{{0,{MAX_CODE_BLOCK_LENGTH}}}?(?:\`\`\`|~~~)\r?\n?"
        rf"|(?:(?:^|\r?\n)(?: {4}|\t)[^\r\n]{{0,{MAX_LIST_ITEM_LENGTH}}}(?:\r?\n(?: {4}|\t)[^\r\n]{{0,{MAX_LIST_ITEM_LENGTH}}}){{0,{MAX_INDENTED_CODE_LINES}}}\r?\n?)"
        rf"|(?:<pre>(?:<code>)?[\s\S]{{0,{MAX_CODE_BLOCK_LENGTH}}}?(?:</code>)?</pre>))"

        rf"|"

        # 5. Tables (Markdown, grid tables, and HTML tables, with length constraints)
        rf"(?:(?:^|\r?\n)(?:\|[^\r\n]{{0,{MAX_TABLE_CELL_LENGTH}}}\|(?:\r?\n\|[-:]{{1,{MAX_TABLE_CELL_LENGTH}}}\|)?"
        rf"(?:\r?\n\|[^\r\n]{{0,{MAX_TABLE_CELL_LENGTH}}}\|){{0,{MAX_TABLE_ROWS}}}"
        rf"|<table>[\s\S]{{0,{MAX_HTML_TABLE_LENGTH}}}?</table>))"

        rf"|"

        # 6. Horizontal rules (Markdown and HTML hr tag)
        rf"(?:^(?:[-*_]){{{MIN_HORIZONTAL_RULE_LENGTH},}}\s*$|<hr\s*/?>)"

        rf"|"

        # 10. Standalone lines or phrases (including single-line blocks and HTML elements, with length constraints)
        rf"(?:^(?:<[a-zA-Z][^>]{{0,{MAX_HTML_TAG_ATTRIBUTES_LENGTH}}}>)?(?:(?:[^\r\n]{{1,{MAX_STANDALONE_LINE_LENGTH}}}(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))|(?:[^\r\n]{{1,{MAX_STANDALONE_LINE_LENGTH}}}(?=[\r\n]|$))|(?:[^\r\n]{{1,{MAX_STANDALONE_LINE_LENGTH}}}(?=[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?:.{{1,{LOOKAHEAD_RANGE}}}(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))?))(?:</[a-zA-Z]+>)?(?:\r?\n|$))"

        rf"|"

        # 7. Sentences or phrases ending with punctuation (including ellipsis and Unicode punctuation)
        rf"(?:(?:[^\r\n]{{1,{MAX_SENTENCE_LENGTH}}}(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))|(?:[^\r\n]{{1,{MAX_SENTENCE_LENGTH}}}(?=[\r\n]|$))|(?:[^\r\n]{{1,{MAX_SENTENCE_LENGTH}}}(?=[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?:.{{1,{LOOKAHEAD_RANGE}}}(?:[.!?…]|\.\.\.|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))?))"

        rf"|"

        # 8. Quoted text, parenthetical phrases, or bracketed content (with length constraints)
        rf"(?:"
        rf"(?<!\w)\"\"\"[^\"]{{0,{MAX_QUOTED_TEXT_LENGTH}}}\"\"\"(?!\w)"
        rf"|(?<!\w)(?:['\"\`\'])[^\r\n]{{0,{MAX_QUOTED_TEXT_LENGTH}}}\\1(?!\w)"
        rf"|\([^\r\n()]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}(?:\([^\r\n()]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}\)[^\r\n()]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}){{0,{MAX_NESTED_PARENTHESES}}}\)"
        rf"|\[[^\r\n\[\]]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}(?:\[[^\r\n\[\]]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}\][^\r\n\[\]]{{0,{MAX_PARENTHETICAL_CONTENT_LENGTH}}}){{0,{MAX_NESTED_PARENTHESES}}}\]"
        rf"|\$[^\r\n$]{{0,{MAX_MATH_INLINE_LENGTH}}}\$"
        rf"|\"[^\"\r\n]{{0,{MAX_MATH_INLINE_LENGTH}}}\""
        rf")"

        rf"|"

        # 9. Paragraphs (with length constraints)
        rf"(?:(?:^|\r?\n\r?\n)(?:<p>)?(?:(?:[^\r\n]{{1,{MAX_PARAGRAPH_LENGTH}}}(?:[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))|(?:[^\r\n]{{1,{MAX_PARAGRAPH_LENGTH}}}(?=[\r\n]|$))|(?:[^\r\n]{{1,{MAX_PARAGRAPH_LENGTH}}}(?=[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?:.{{1,{LOOKAHEAD_RANGE}}}(?:[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))?))(?:</p>)?(?=\r?\n\r?\n|$))"

        rf"|"

        # 11. HTML-like tags and their content (including self-closing tags and attributes, with length constraints)
        rf"(?:<[a-zA-Z][^>]{{0,{MAX_HTML_TAG_ATTRIBUTES_LENGTH}}}(?:>[\s\S]{{0,{MAX_HTML_TAG_CONTENT_LENGTH}}}?</[a-zA-Z]+>|\s*/>))"

        rf"|"

        # 12. LaTeX-style math expressions (inline and block, with length constraints)
        rf"(?:(?:\$\$[\s\S]{{0,{MAX_MATH_BLOCK_LENGTH}}}?\$\$)|(?:\$[^\$\r\n]{{0,{MAX_MATH_INLINE_LENGTH}}}\$))"

        rf"|"

        # 14. Fallback for any remaining content (with length constraints)
        rf"(?:(?:[^\r\n]{{1,{MAX_STANDALONE_LINE_LENGTH}}}(?:[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))|(?:[^\r\n]{{1,{MAX_STANDALONE_LINE_LENGTH}}}(?=[\r\n]|$))|(?:[^\r\n]{{1,{MAX_STANDALONE_LINE_LENGTH}}}(?=[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?:.{{1,{LOOKAHEAD_RANGE}}}(?:[.!?…]|\.{3}|[\u2026\u2047-\u2049]|[\p{{Emoji_Presentation}}\p{{Extended_Pictographic}}])(?=\s|$))?))"
        ,
        regex.MULTILINE | regex.UNICODE
    )
    chunks = pattern.findall(text)
    return list(filter(lambda x: x != "", chunks))