# TRELL-IMT 2024
TAF DCL
UE WEB

# Objectives 

The project proposed this year consists of developing a dynamic web application for
tracking projects and tasks, inspired by tools like Trello. This application will be designed
to facilitate collaboration between team members on projects
development, by offering an intuitive platform to organize, track, and manage the work of
efficient manner.

# Project Setup :

This section guides you through the process of getting your development environment set up for Trell'IMT.

### Prerequisites
Ensure you have the following installed:

Python 3.7 or higher  
pip (Python package manager)  
Git (Version control system)  

### Installation
Clone the repository

git clone https://github.com/antoinech2/Trell-IMT  
cd TrellIMT

### Set up a virtual environment

##### For Windows:
python -m venv venv  
.\venv\Scripts\activate

##### For macOS and Linux:
python3 -m venv venv  
source venv/bin/activate

### Install required Python packages
pip install -r requirements.txt

### Database Initialization
The application uses SQLAlchemy to manage and initialize the database. Upon the first run, SQLAlchemy will create the database and the required tables.

### Running the Application
To run the application locally, use Flask's built-in server:

#### Set the environment variables

##### For Windows:
set FLASK_APP=run.py  
set FLASK_ENV=development  
##### For macOS and Linux:
export FLASK_APP=run.py  
export FLASK_ENV=development  

#### Start the Flask development server
flask run  

This will start the server on http://127.0.0.1:5000/ by default.

# Database Schema : 

### User
id: INTEGER - A unique identifier for each user.  
first_name: VARCHAR(50) - The user's first name.  
last_name: VARCHAR(50) - The user's last name.  
email: VARCHAR(120) - The user's email address.  
type: VARCHAR(14) - The user's type or role within the application.  
password: VARCHAR - The user's hashed password.  
authenticated: BOOLEAN - Indicates if the user is authenticated.  
language: VARCHAR(7) - The user's preferred language.  
### Board
id: INTEGER - Unique identifier for each board.  
name: VARCHAR - The name of the board.  
description: VARCHAR - A brief description of the board.  
### BoardUsers
user_id: INTEGER - References the user table to associate users with boards.  
board_id: INTEGER - References the board table to associate boards with users.  
### Category
id: INTEGER - Unique identifier for each category.  
board_id: INTEGER - References the board table to categorize boards.  
name: VARCHAR - The name of the category.  
description: VARCHAR - A brief description of the category.  
### Task
id: INTEGER - Unique identifier for each task.  
category_id: INTEGER - References the category table to categorize tasks.  
name: VARCHAR - The name of the task.  
description: VARCHAR - A brief description of the task.  
date_expires: DATETIME - The expiration date for the task.  
priority: INTEGER - The priority of the task.  
### EtiquetteTask
task_id: INTEGER - References the task table to associate tasks with etiquettes.  
etiquette_id: INTEGER - References the etiquette table to associate etiquettes with tasks.  
### UserTask
task_id: INTEGER - References the task table to associate tasks with users.  
user_id: INTEGER - References the user table to associate users with tasks.  
association_type: VARCHAR(8) - The type of association between the user and the task (e.g., owner, collaborator).  
### Step
id: INTEGER - Unique identifier for each step.  
task_id: INTEGER - References the task table to associate steps with tasks.  
status: BOOLEAN - Indicates if the step is completed.  
name: VARCHAR - The name of the step.  
description: VARCHAR - A brief description of the step.  
### Commentary
id: INTEGER - Unique identifier for each commentary.  
task_id: INTEGER - References the task table to associate commentaries with tasks.  
user_id: INTEGER - References the user table to indicate who made the commentary.  
title: VARCHAR - The title of the commentary.  
content: VARCHAR - The content of the commentary.  
date_created: DATETIME - The date when the commentary was created.  
### Etiquette
id: INTEGER - Unique identifier for each etiquette.  
type: VARCHAR - The type of etiquette.  
label: VARCHAR - The label of the etiquette.  
description: VARCHAR - A brief description of the etiquette.  
color: VARCHAR - The color associated with the etiquette.  

# Project structure

Trell'IMT is structured into various directories and files for optimal organization and modularity. 
Below is the breakdown of the major components:

### /data
Contains JSON templates and other data files that are crucial for initializing the application's state.  

new_board_template.json: This file contains the JSON template for creating new boards within the application.
### /instance
Holds configuration files and local databases that are specific to the instance of the application.

database.db: A SQLite database file that contains all the application's data.
### /src
The source directory where the main application code resides, organized into subdirectories for database models, form handling, and helper functions.

### /database
Includes scripts related to database initialization and structure.

data_init.py: Script to initialize database with default data.  
database.py: Contains database connection configurations and initializations.  
models.py: Defines the ORM models for SQLAlchemy.  
### /form
Contains Python scripts to handle form submissions for various actions within the application.

delete_board.py, delete_category.py, delete_task.py: Scripts to handle the deletion of boards, categories, and tasks, respectively.  
edit_board.py, edit_category.py, edit_task.py: Scripts for editing boards, categories, and tasks.  
new_category.py, new_comment.py, new_task.py: Scripts to create new categories, comments, and tasks.  
### /helper
Houses utility scripts that provide auxiliary functionality to the main application logic.

date.py: Functions related to date manipulation.  
get_board_info.py, get_etiquettes.py, get_task_display.py, get_task_info.py, get_users.py: Scripts to retrieve specific pieces of information from the database.  
login.py, logout.py: Handle user authentication sessions.  
### /routes
Contains Python scripts defining the Flask routes for the application's different URLs.

board_dev.py, board_manager.py, home.py: Scripts responsible for the board development, management interfaces, and the home page.  
new_project.py, sign_in.py, sign_up.py: Handle project creation and user authentication processes.  
### /static
This directory serves all static content, such as CSS, JavaScript, and image files.

#### /static/css
Contains CSS files that define the styling for the application.

auth.css, board.css, dev.css, home.css: Style sheets for authentication forms, board view, developer tools, and the home page, among others.
#### /static/img
Stores image files used within the application.

logo.jpg, logo_site_page.jpg: Logos and branding-related images.
#### /static/js
Includes JavaScript files that add interactivity to the application.

collab.js, etiquette.js, subtasks.js, task_form.js: Scripts that manage collaboration features, etiquettes, subtasks, and task forms.
add_category.js, delete_board.js, modify_board.js, modify_category.js, project_creator.js, utils.js: Utility scripts for modifying application data and managing project creation.
### /templates
Holds Jinja2 templates which define the HTML structure for rendering views.

#### /templates/components
Reusable components that are included across various templates.

board_form.html.jinja2, category_form.html.jinja2: Templates for forms used in board and category management.  
header.html.jinja2, super_header.html.jinja2: Header templates for standard and extended navigation.  
task_form.html.jinja2, warning_delete.html.jinja2: Templates for task-related forms and deletion warnings.  
#### /templates/developer
Templates specific to the developer view.

board_developer.html.jinja2: The developer's board view template.
#### /templates/project_manager
Templates for project management views.

# Contributors :

CHEUCLE Antoine  
SOJKA Emmanuelle  
CLAEYS Nathan  