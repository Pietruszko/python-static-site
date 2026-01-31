def extract_title(markdown):
    lines = markdown.split('\n')
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# ') and len(stripped) > 2:
            return stripped[1:].strip()
    
    raise Exception("No h1 header found")
