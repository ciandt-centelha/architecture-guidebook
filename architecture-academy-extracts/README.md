# Google Slides to Markdown Conversion Scripts

This project contains Python scripts that help you extract content from Google Slides presentations and convert them into Markdown format. These scripts are designed to work in tandem with Google's in-browser API client to avoid auth requirements for accessing the API via scripts.

## Prerequisites

Before using the scripts, ensure that you have the following:

1. **Python 3.x** installed on your machine.

## How to Use the Scripts

### Step 1: Create an Empty JSON File for the Presentation

1. **Run the Script**:
   - Execute the `url_to_json_file.py` script:
     ```bash
     python save_json.py
     ```

2. **Provide the Google Slides URL**:
   - The script will prompt you to enter the URL of the Google Slides presentation.

3. **Specify the Output File Name**:
   - Next, you will be asked to provide a name for the JSON file where the presentation data will be saved.
   - This file will be created in the `../json` directory.

### Step 2: Fetch the JSON Data Using the Presentation ID

1. **Access Google Slides API**:
   - Go to the [Google Slides API Docs page for the GET Presentation request](https://developers.google.com/slides/api/reference/rest/v1/presentations/get). Launch the API client from the right hand sidebar.
     - _Preferably, use a real API client or script to execute these requests. However, getting the requisite auth credentials requires creating a GCP project, which you may not be authorized to do._

2. **Use the Presentation ID**:
   - When making the API request, use the `presentationId` printed by the script in Step 1.

3. **Copy the JSON Response**:
   - Copy the JSON data returned by the API.

### Step 3: Paste the JSON Data into the File

1. **Open the JSON File**:
   - Open the JSON file created in Step 1 (located in the `../json` directory).

2. **Paste the JSON Data**:
   - Replace the empty JSON object `{}` in the file with the JSON data you copied in Step 2.

3. **Save the File**:
   - Save the changes to the file.

### Step 4: Convert the JSON to Markdown

1. **Run the Conversion Script**:
   - Execute the main conversion script to process the JSON files and convert them into Markdown.
   ```bash
   python main.py
   ```

2. **Markdown Output**:
   - The script will read each JSON file from the `../json` directory, process it, and save the corresponding Markdown file in the `../md` directory.
   - If the Markdown file already exists, it will be overwritten.

### Example Workflow Recap

1. Use the `url_to_json_file.py` script to create an empty JSON file and get the presentation ID.
2. Fetch the JSON data from the Google Slides API using the provided ID.
3. Paste the JSON data into the JSON file.
4. Run the conversion script to generate Markdown files.

---

### Supported Parsing Features

- **Headers**: The script automatically maps font sizes to headers (H1, H2, H3). This attempts to match the styling in the Google Slides as closely as possible.
- **Table Formatting**: The script handles table formatting.
- **Images**: Any images in the slides are linked in the Markdown output using the appropriate URL.

### Known Problems

- **Bulleted Lists Not Converting**: Ensure that paragraphs are correctly identified as bullet points in the JSON.
- **Tables with Merged Cells**: The script may not handle tables with merged cells correctly. Columns are liable to be dropped.

