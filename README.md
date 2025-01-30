
<h1 align="center" style="font-weight: bold;">My C$50 Finance</h1>

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python Badge">
  <img src="https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white&style=for-the-badge" alt="Flask Badge">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5 Badge">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite Badge">
</div>

#

_Other versions:_
[_Clique aqui para Português_](./README-ptBR.md)

<h4 align="center"> 
     Status: Finished
</h4>

<p align="center">
 <a href="#about-ℹ️">About</a> •
 <a href="#features-🌟">Features</a> •
 <a href="#project-demonstration-🖥️">Demonstration</a> •
 <a href="#application-architecture-🏗️">Application Architecture</a> •
 <a href="#setup-⚙️">Setup</a>  • 
 <a href="#author-👨🏻‍💻">Author</a> •
 <a href="#license-📝">License</a>
</p>

#

<h6 align="justify"><b>Important Disclaimer:</b> This project was developed as part of the CS50x course. If you are currently taking the course, please do not view or copy this code, as it may violate the course's academic honesty policy. Use this repository for reference only after you have completed the course.
</h6>

#

## About ℹ️
C$50 Finance is a web application built using Flask  that allows users to simulate stock trading. Users can register and log in with a unique username and password. The app fetches current stock prices and enables users to buy, sell, or hold stocks. It maintains a transaction history for each user, tracking their portfolio and updating it based on real-time stock price changes. Additionally, users can add more money to their account and change their passwords. The application was originally built using an API endpoint that provided CSV data, which is no longer available. Because of that, it has been adjusted to use a new API endpoint that returns JSON data. 

## Features 🌟
- User registration and authentication
- Simulate buying and selling stocks with current prices
- View transaction history
- Manage portfolio and view current stock prices
- Add cash to user account
- Allows users to change password


## Project Demonstration 🖥️
[see the demonstration here](https://youtu.be/nAXZgyfQJnw)

## Application Architecture 🏗️

The backend is designed using Flask and SQLite. The main modules include:
- `app.py`: Contains the main application routes and logic.
- `helpers.py`: Contains helper functions for the application, including the `lookup` function to query stock prices.
- `templates/`: Contains HTML templates for rendering the web pages. It uses a layout template and Jinja to dynamically generate the content.
- `static/`: Contains static files like CSS for styling.

### Data Flow
1. **User Registration/Login**: Users can register and log in to the application.
2. **Stock Transactions**: Users can buy and sell stocks. The application queries the Yahoo Finance API to get the latest stock prices.
3. **Portfolio Management**: Users can view their portfolio, including the current value of their stocks and transaction history.
4. **Database**: All user data, transactions, and stock information are stored in an SQLite database.

## Setup ⚙️
To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rafaelmeller/finance-cs50.git
   cd finance-cs50
   ```

2. **Create a virtual environment (Mac)**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   flask run
   ```

## Author 👨🏻‍💻

#### Rafael Meller, CS50 Staff
<h6><i>This project was a problem set for HarvardX's Introduction to Computer Science course (CS50x), being partially developed by the CS50 staff and then finished by Rafael Meller</i></h6>

[![Linkedin Badge](https://img.shields.io/badge/-Rafael_Meller-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/tgmarinho/)](https://www.linkedin.com/in/rafaelmeller/) 
[![Gmail Badge](https://img.shields.io/badge/-rafaelmeller.dev@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=rafaelmeller.dev@gmail.com)](mailto:rafaelmeller.dev@gmail.com)

## License 📝

This project is licensed under the [MIT](./LICENSE) License. The original problem set is the property of CS50.
