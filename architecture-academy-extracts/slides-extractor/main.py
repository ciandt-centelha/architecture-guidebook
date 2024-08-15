import json
import os

# Define input and output directories
input_dir = os.path.join('..', 'json')
output_dir = os.path.join('..', 'md')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def map_font_size_to_header(font_size):
    """Map font size to markdown header level."""
    if font_size >= 32:
        return "# "  # H1
    elif 24 <= font_size < 32:
        return "## "  # H2
    elif 17 <= font_size < 24:
        return "### "  # H3
    else:
        return ""  # Normal text

def parse_text_element(text_element, bullet_prefix=""):
    """Parse a text element and return the content with appropriate Markdown formatting."""
    content = ""
    if 'textRun' in text_element:
        text_run = text_element['textRun']
        font_size = text_run.get('style', {}).get('fontSize', {}).get('magnitude', 12)
        header_prefix = map_font_size_to_header(font_size)
        text_content = text_run['content'].strip()

        # Ensure headers start on a new line and prevent empty headers
        if header_prefix and text_content:
            content += f"\n{header_prefix}{text_content}\n"
        else:
            content += f"{bullet_prefix}{text_content}\n"
    return content

def parse_table(table):
    """Parse a table object into Markdown format."""
    table_markdown = ""
    rows = table.get('tableRows', [])
    for row in rows:
        row_content = "|"
        for cell in row.get('tableCells', []):
            cell_text = ""
            if 'text' in cell:
                for text_element in cell['text'].get('textElements', []):
                    cell_text += parse_text_element(text_element)
            row_content += f" {cell_text.strip()} |"
        table_markdown += row_content + "\n"
    # Create header separator for markdown tables
    if rows:
        header_separator = "|"
        for _ in rows[0].get('tableCells', []):
            header_separator += " --- |"
        table_markdown = table_markdown.split("\n", 1)[0] + "\n" + header_separator + "\n" + table_markdown.split("\n", 1)[1]
    return table_markdown

def parse_paragraph_marker(paragraph_marker, nesting_level=0):
    """Parse paragraph markers to detect and format lists."""
    bullet_prefix = ""
    if 'bullet' in paragraph_marker:
        # Determine bullet prefix based on nesting level
        bullet_prefix = "  " * nesting_level + "- "
    return bullet_prefix

# Process each .json file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        input_path = os.path.join(input_dir, filename)
        output_filename = filename.replace('.json', '.md')
        output_path = os.path.join(output_dir, output_filename)

        # Load the JSON data from the file
        with open(input_path, 'r') as file:
            presentation = json.load(file)

        # Extract title and slides
        presentation_id = presentation.get('presentationId', 'unknown_id')
        title = presentation.get('title', 'Untitled Presentation')
        slides = presentation.get('slides', [])

        # Construct the URL to the Google Slides presentation
        presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/view"

        # Initialize markdown content
        markdown_content = f"Extracted from: [{presentation_url}]({presentation_url})\n\n"
        markdown_content += f"# {title}\n\n"

        # Iterate through each slide
        for i, slide in enumerate(slides, start=1):
            elements = slide.get('pageElements', [])

            # Add slide number
            markdown_content += f"## Slide {i}\n\n"

            # Extract content from each element
            for element in elements:
                if 'shape' in element:
                    text_elements = element['shape'].get('text', {}).get('textElements', [])
                    for text_element in text_elements:
                        bullet_prefix = ""
                        if 'paragraphMarker' in text_element:
                            bullet_prefix = parse_paragraph_marker(text_element['paragraphMarker'])
                        markdown_content += parse_text_element(text_element, bullet_prefix)

                elif 'image' in element:
                    image_url = element['image'].get('contentUrl', '')
                    if image_url:
                        markdown_content += f"![Image]({image_url})\n"
                        if element.get('title'):
                            markdown_content += f"*Title: {element['title']}*\n"
                        if element.get('description'):
                            markdown_content += f"*Description: {element['description']}*\n"

                elif 'table' in element:
                    markdown_content += parse_table(element['table']) + "\n"

            markdown_content += "\n\n"  # Add space between slides

        # Write to a markdown file
        with open(output_path, 'w') as f:
            f.write(markdown_content)

        print(f"Markdown content generated for {filename}, saved to {output_path}.")