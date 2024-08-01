Project Title: Document Understanding Model with Gemini Flash
Overview
This project focuses on fine-tuning the Gemini 1.5 Flash model for effective text extraction from various document formats. The application is built using Python and Streamlit, providing an interactive web interface for users to upload documents and retrieve extracted text. The training and fine-tuning processes are conducted using Google AI Studio, leveraging its powerful machine learning capabilities.

Table of Contents:

    Installation
    Setup
    Usage
    Project Structure
    Training and Fine-tuning
    Contributing
    License

Installation
To set up the project, ensure you have the following prerequisites:

    Python 3.8 or higher
    pip (Python package installer)
    Access to Google Cloud Platform with Vertex AI enabled

Clone the repository:

bash

git clone https://github.com/Optimus-Technologies/Document-Understand.git

cd udocx-prototype

Install the required packages:

bash
pip install -r requirements.txt

Setup

    Google Cloud Configuration:
        Set up a Google Cloud project.
        Enable the Vertex AI API.
        Create a service account with the necessary permissions and download the JSON key file.
        Set the environment variable for authentication:

    bash
    export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-file.json"

Streamlit Configuration:

    Ensure that Streamlit is installed. If not, install it using pip:

bash
pip install streamlit

Usage
To run the application, execute the following command:

bash
streamlit run main.py

This will start a local server, and you can access the application in your web browser at http://localhost:8501.
Project Structure

text
udocx-prototype/
│
├── main.py                  # Main application file
├── functions.py             # Contains the main functions for interracting with the model
├── model.py                 # Contains the model and prompts
├── parser.py                # Contains the convertors for handling multiple file types
├── documents.txt            # A temporary file for holding data

Training and Fine-tuning
The training and fine-tuning of the Gemini model are done in Google AI Studio. Follow these steps:

    Prepare Your Dataset:
        Organize your training data in a suitable format (e.g., CSV, JSON) that includes the documents and their respective labels.
    Train the Model:
        Use the train_model.py script to initiate the training process. Ensure that you specify the correct parameters for your dataset and model configuration.
    Fine-tune the Model:
        After the initial training, use finetune_model.py to further refine the model on specific tasks or datasets.

Contributing
Contributions are welcome! Please follow these steps to contribute:

    Fork the repository.
    Create a new branch for your feature or bug fix.
    Make your changes and commit them.
    Push your branch to your forked repository.
    Create a pull request detailing your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details. This README provides a comprehensive guide to setting up and using the Document Understanding Model with Gemini Flash. For any issues or inquiries, please open an issue in the GitHub repository.
