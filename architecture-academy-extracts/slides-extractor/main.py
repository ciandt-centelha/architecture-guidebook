import json
import os
from mdutils.mdutils import MdUtils

# Define input and output directories
input_dir = os.path.join('..', 'json')
output_dir = os.path.join('..', 'md')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def map_font_size_to_header(font_size):
    """Map font size to markdown header level."""
    if font_size >= 32:
        return 1  # H1
    elif 24 <= font_size < 32:
        return 2  # H2
    elif 17 <= font_size < 24:
        return 3  # H3
    else:
        return 0  # Normal text

def parse_text_element(md_file, text_element, bullet_prefix=""):
    """Parse a text element and add the content with appropriate Markdown formatting."""
    if 'textRun' in text_element:
        text_run = text_element['textRun']
        font_size = text_run.get('style', {}).get('fontSize', {}).get('magnitude', 12)
        header_level = map_font_size_to_header(font_size)
        text_content = text_run['content'].strip()

        if header_level > 0:
            md_file.new_header(level=header_level, title=text_content)
        else:
            if bullet_prefix:
                md_file.new_list([f"{bullet_prefix}{text_content}"])
            else:
                md_file.new_paragraph(text_content)

def parse_table(md_file, table):
    """Parse a table object into Markdown format."""
    rows = table.get('tableRows', [])
    if not rows:
        return

    # Extract table data
    table_data = []
    for row in rows:
        row_content = []
        for cell in row.get('tableCells', []):
            cell_text = ""
            if 'text' in cell:
                for text_element in cell['text'].get('textElements', []):
                    if 'textRun' in text_element:
                        cell_text += text_element['textRun']['content'].strip()
            row_content.append(cell_text)
        table_data.extend(row_content)

    # Determine number of columns
    num_columns = len(rows[0].get('tableCells', []))

    # Add table to markdown
    md_file.new_table(columns=num_columns, rows=len(rows), text=table_data, text_align='center')

def parse_paragraph_marker(paragraph_marker):
    """Parse paragraph markers to detect and format lists."""
    bullet_prefix = ""
    if 'bullet' in paragraph_marker:
        # Determine bullet prefix based on nesting level
        bullet_prefix = "  " + "- "
    return bullet_prefix

# Process each .json file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        input_path = os.path.join(input_dir, filename)
        output_filename = filename.replace('.json', '')
        output_path = os.path.join(output_dir, output_filename + ".md")

        # Load the JSON data from the file
        with open(input_path, 'r') as file:
            presentation = json.load(file)

        # Extract title and slides
        presentation_id = presentation.get('presentationId', 'unknown_id')
        title = presentation.get('title', 'Untitled Presentation')
        slides = presentation.get('slides', [])

        # Construct the URL to the Google Slides presentation
        presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/view"

        # Initialize mdutils and add introductory content
        md_file = MdUtils(file_name=output_path)
        md_file.new_paragraph(f"Extracted from: [{presentation_url}]({presentation_url})")
        md_file.new_header(level=1, title=title)

        # Iterate through each slide
        for i, slide in enumerate(slides, start=1):
            md_file.new_header(level=2, title=f"Slide {i}")

            elements = slide.get('pageElements', [])
            for element in elements:
                if 'shape' in element:
                    text_elements = element['shape'].get('text', {}).get('textElements', [])
                    for text_element in text_elements:
                        bullet_prefix = ""
                        if 'paragraphMarker' in text_element:
                            bullet_prefix = parse_paragraph_marker(text_element['paragraphMarker'])
                        parse_text_element(md_file, text_element, bullet_prefix)

                elif 'image' in element:
                    image_url = element['image'].get('contentUrl', '')
                    if image_url:
                        md_file.new_paragraph(f"![Image]({image_url})")
                        if element.get('title'):
                            md_file.new_paragraph(f"*Title: {element['title']}*")
                        if element.get('description'):
                            md_file.new_paragraph(f"*Description: {element['description']}*")

                elif 'table' in element:
                    parse_table(md_file, element['table'])

        # Save the markdown file
        md_file.create_md_file()

        print(f"Markdown content generated for {filename}, saved to {output_path}.")