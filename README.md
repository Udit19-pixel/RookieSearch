
# RookieSearch

# Project Description

A project based demonstration that creates RAG based system that answers questions based on official Python Documentation. 

# Project Requirements

- A virtual environment for project isolation.
- Python LTS version.
- An Integrated Development Environment (preferably Visual Studio Code).

# Features

### The essential features of this project are -
- A RAG based system for retrieval of best possible context from the index.faiss file, generated from the documentation.
- Checkpoints incorporated in order to avoid momentarily stoppage in index generation. 
- Preprocessing of the final JSON-formatted file in particular format.
- Developing a React based front-end for user interaction.
- Email alerts in case if resource limit is exceeded.
- Evaluation script that analyzes how effective the pipeline is.
- Test scripts to maintain the integrity of the project. 

# Project Structure and Build

## Directory Structure
- The Directory contains various types of models and respective views depending upon the requirements for each template.
<div align="center">
 <img src="https://github.com/Udit19-pixel/RookieSearch/blob/main/Project_Structure.png" alt="Project Structure" width="280" height="300">
</div>

## Environment and Run Procedure
 - The first step is to create a virtual environment for the project and making that as running the activate.bat file present in the bin/Scripts folder. This is to activate the environment created (you might notice "(env)" before the directory path) -

     ```
        Step - I : python -m venv env
        Step - II :
            # for macOS -
            - source env/bin/activate
            # for windows -
            - env/bin/activate
    ```
 - When the virtual environment has been created successfully, go the directory in your local machine where the setup_project.bat file is present and type the same in your terminal, hit enter.

- Install the node dependencies in the rookiesearch-frontend folder by the following command -
    ```
        npm install
    ```
- Additionally, if one wants to monitor how much resource this project is consuming (to check if the coded-limit exceeds), the monitoring.py file can be run, which logs the details into rookiesearch.log file every 5 minutes, using following command -
    ```
        python searchAPI.py
    ```
- When the above commands are executed concurrently, one can land on the page and ask their question. Here is a sample case -
<div align="center">
 <img src="https://github.com/Udit19-pixel/RookieSearch/blob/main/Asking%20Question.png" alt="Asking question" width="280" height="300">
</div>


## Principles of Retrieval Augmented Generation (RAG)
- Combination of Retrieval and Generation: RAG leverages both retrieval-based and generation-based models. It retrieves relevant documents or snippets from a large corpus and then generates a coherent and contextually appropriate response based on the retrieved information.

- Enhanced Knowledge Utilization: By incorporating retrieval, RAG can access and utilize a broader knowledge base, making it more effective in providing accurate and detailed responses, especially for complex or specific queries.

- Improved Answer Accuracy: The retrieval component ensures that the generated answers are grounded in actual data or documents, thereby improving the factual accuracy and reliability of the responses.

- Scalability and Flexibility: RAG systems can be scaled to handle large volumes of data and diverse types of queries, making them versatile tools for various applications, from customer support to technical documentation assistance.

## Project Working - RAG Pipeline
- First of all, if you haven't, try going through the RAG pipeline diagram that was created using draw.io
- The diagram included various components that were put together into making this project.
- The front-end is made using React with minimalistic design (the focus was actually on the pipelining, so user experience was cut-short).
- Whenever user asks a question related to python, that question is then checked upon against the FAISS index that is created from the official documentation and vector_store.py script, through an embedding model (in this case all-MiniLM-L6-v2).
- Then, the best possible context is found under certain parameters and constraints, which is then posted to the front-end.
- Simultaneously, the test_rookiesearch.py script under the tests folder, helps to rectify any missing imports and if the application is working correctly.
- For example, the question that was asked above might reply differently everytime it's searched for and can also behave abruptly. In case if it doesn't find relevant answer, a different message is posted.
- The preprocessing wasn't done upto the mark because of machine limitations. Also, the final JSON preprocessed file took around 3.5 hours of time to get ready, even after using torch library and more efficient scripts. Look into the answer that was generated -
<div align="center">
 <img src="https://github.com/Udit19-pixel/RookieSearch/blob/main/Answer%20Generated.png" alt="Answer generated" width="280" height="300">
</div>


## Project Working - Miscellaneous features
- One thing that was achieved in amidst of making this project, was setting up email notification, whenever certain limit hits. This was done using SMTP protocols and setting up app passwords (look up in the internet, on how to do so).
- Below is the sample email script that was tested created in order to achieve so (obviously, one can't show their identity essentials, as a result of  which, the file is not present in this repository) -
<div align="center">
 <img src="https://github.com/Udit19-pixel/RookieSearch/blob/main/Email%20Notification-1.png" alt="Email notification-1" width="280" height="300">
</div>

- Once, the script is executed, the following can be seen in the mail server -
<div align="center">
 <img src="https://github.com/Udit19-pixel/RookieSearch/blob/main/Email%20Notification-2.png" alt="Email notification-2" width="280" height="300">
</div>

- In addition to this, a file named rookiesearch.log willbe created which not only shows the disk stats, but also logs what was asked initially. The same logs onto the terminal once the searchAPI.py script is run.
<div align="center">
 <img src="https://github.com/Udit19-pixel/RookieSearch/blob/main/rookiesearch-log.png" alt="Log file" width="280" height="300">
</div>
