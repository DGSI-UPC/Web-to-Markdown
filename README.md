# Web-to-Markdown
The purpose of this project is to be able to convert the information from any website into a Markdown bucket.

## Installation and setup

1. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

3. Access the API documentation at `http://127.0.0.1:8000/docs`

## Usage
This website has a UI with a text field in the middle. Enter the base URL of the website you want to extract information from and it will automatically find all the attached links to it and also extract information from them.

To extract this information we get the HTML using the library trafilatura and parse it using BeautifulSoup and html2text.