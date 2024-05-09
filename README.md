# Flask Blog

Welcome to the Flask Blog, a lightweight and customizable blogging platform built using Flask, a popular Python web framework. This blog allows users to create, publish, and manage content easily.

## Features
- **User-friendly Interface**: The Flask Blog provides a clean and intuitive user interface for writing and managing blog posts.
- **Logging In**: You can log in and use the platform, no worries the passwords are hashed using flask-bcrypt
- **Password recovery**: You can reset your password if you forget or lose it
- **Easy Installation**: Follow the steps below to quickly set up and install Flask and other required libraries:

## Installation Guide

1. **Clone Repository**: Clone the Flask Blog repository to your local machine using the following command:

   ```bash
   git clone https://github.com/dkkinyua/flask-blog.git
   ```

2. **Download Required Packages and Modules**: You can install the used modules and packages in this project by accessing the 'requirements.txt' in the directory:

  ```bash

  cd flask-blog
  pip install -r requirements.txt

  ```
This will install all the required modules used for this project.

3. **Run the development server**: You can run the development server on your browser by navigating to the folder containing the 'run.py' file and running the following command:

   ``` python
   
   cd flask-blog
   flask --app run run --debug

   ```
   **NOTE** Running the development server using the "--debug" option helps you in debugging from the browser using a special console, you will be provided with a debugging key to do so. See the photo below.

   ![image](https://github.com/dkkinyua/flask-blog/assets/67056891/13c05e9f-859f-4fd9-9932-5bbe633cba37)

  Once your server is running, visit HTTP://localhost:5000 to access Flask Blog.

**Contributions:**

If you'd like to contribute to the Flask Blog project, feel free to fork the repository, make changes, and submit a pull request. Contributions are always welcome!


