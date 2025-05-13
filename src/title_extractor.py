def extract_title(markdown):
    """
    Pull the h1 header from markdown and return it.
    Raises an exception if no h1 header is found.
    """
    lines = markdown.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")