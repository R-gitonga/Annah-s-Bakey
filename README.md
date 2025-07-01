# Annah's Bakery

This is a delightful web application buitl with Flask, designed to showcase freshly baked goods. This project provides a foundationa; e-commerce-like display, focusing on clean desing and responsive user experience.

* [Features](#features)
* [Technologies used](#technologies-used)
* [Design Resources](#design-resources)
* [Project Structure](#project-structure)
* [Setup and Installation](#setup-and-installation)
* [Database Management](#database-management)
* [Future Enhancements](#future-enhancements)
* [License](#license)

#features
* **Dynamic Product Display**: Fetches and displays product information directly form SQLite database
* **Hero Section**: prominent welcome section with a background image, overlay text, and a call-to-action button
* **Responsive Navigation Bar**: Features a gradient background, brand titke, and navigation links, designed to adapt to various screen sizes using Bootstrap.
* **Product Grid**: Products are displayed in a responsive grid layout using Bootstrap's grid system, adjusting colum counts based on screen size
* **Smooth Scroll Anchor**: The 'Browse Menu' button uin the hero section smoothly scrolls to the "Featured Products" section.
* **Database Intergration**: Uses SQLite for simple and efficient data storage.

#technologies-used
* **Backend Framework**: [Flask(Python)](https://flask.palletsprojects.com/en/stable/)
* **Database**: [SQLite3](https://sqlite.org/index.html)
* **Templating Engine**: [jinja2](https://jinja.palletsprojects.com/en/stable/)
* **Frontend Framework**:[ Bootstrap 5.3](https://getbootstrap.com/)
* **Version Control**: [Git](https://git-scm.com/downloads)

#design-resources
To aid in the design and planning phases of this project, the following tools were utilized
* **Figma (Design Prototype)**: Used for creating the initial UI/UX design and mockups for the application's layout and visual elements.
    [Annah's Bakery Figma Design](https://www.figma.com/design/GLuq36nJJyR3JjDxGlYlxk/Annah-s-Bakery?node-id=16-153&m=dev&t=SamXmvDEVVWDFdMm-1)

* **Excalidraw (WireFrame and Database Tables)**: used to create the original wireframe and visualize the database tables.
    [Wireframe and Database Tables](https://excalidraw.com/#json=iX84712tmU8o82IcS4Gty,Hq0oUYtNSmy5L_NdZWXIPA)

* **Gleel.io (Entity Relationship Diagram visualizer)**: Used to visualize the relationships between various tables in the database.
    [Entity Relatuonship Diagram](https://app.gleek.io/diagrams/-2Xn1HDkrv6RUOMJ1Idbqw)

#project-structure
Annah's Bakery/
|---.annah/     # python virtual environemnt
|---data/
    |---bakery.db       # SQLite Database file
|---static/
    |---css/
        |---style.css
    |---images/     # All static image assets
        |---all_images.jpg
    |--- js/        #Javascript files
|---templates/
    |---base.html       # base layout template 
    |---index.html      # homepage template
|---app.py      #Main FLask application file
|---.gitignore  #intentionally untracked files to be ignored by Git
|---README.md   #This file
|---requirements.txt #list python dependencies for this project

#setup-and-installation
**prerequisites**
Python 3.x installed
Git installed.

1. **Clone the Repository**
    git clone https://github.com/R-gitonga/Annah-s-Bakey.git
    cd Annah-s-Bakey

2. **Create and activate a virtual environment**
Although not necessary it is highly recommended to use virtual environments to manage project dependencies
        python -m venv .annah(or whatever name you fancy usually .venv is fine)
        .annah\scripts\activate

3. **Install Dependencies**
Install Flask and other required python packages using pip
    pip install Flask
    pip freeze > requirements.txt (use this command to install dependecies used on this project. ensure virtual environment is on)

4. **Set Flask Environement Variables**
Tell Flask where your application file is.
    **On Windows (Command Prompt)**:
        set FLASK_APP=app.py
    **On Windows (PowerShell)**:
        $env:FLASK_APP = "app.py"

5. **Run the Application**
Start the Flask development server in debug mode.
    flask run --debug

#database-management
The project uses an SQLite database(bakery.db) located in the data/ directory

* **Data Storage**: Product information is stored here.
* **Management Tool**: You can use a tool like **DB Browser for SQLite** to inspect, modify, or add data to the database.

#future-enhancements
1. **Dedicated Product Detail Pages**: Users will be able to click on a product and view more details on a separate page.
2. **Shopping Cart Functionality**: Allow users to add products to a cart and proceed to checkout.
3. **Admin Panel**: Create a Simple interface to add, edit, or delete products in the database.
4. **User Authentication**: Implement user login/registration.
5. **Improve Search/Filtering**: Add functionality to search for products or filter by category.
6. **Deployment**: Prepare the application for deployemnt to a live server.

#license
This project is open-source and availabe under the MIT License.




