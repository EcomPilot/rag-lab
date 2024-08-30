from raglab.chunk.regex_text_chunker import simple_chunker

filename = "./examples/documents/Gullivers-travels-A-Voyage-to-Lilliput.txt"
with open(file=filename, encoding='utf-8') as f:
    entire_document = f.read()
    chunks = simple_chunker(entire_document)
    print(chunks)