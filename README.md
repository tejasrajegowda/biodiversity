# Biodiversity Monitoring System

## Project Overview
The **Biodiversity Monitoring System** is a web application designed to monitor and analyze biodiversity data across various ecosystems. This system allows users to track species population, environmental factors, and ecosystem health using a user-friendly interface. The application leverages technologies like Python, Flask, MySQL, and HTML.

## Features
- **Species Data Management**: Add, update, and manage species data.
- **Ecosystem Monitoring**: Monitor environmental variables impacting biodiversity.
- **Data Visualization**: View trends and reports.
- **User Authentication**: Secure login and user roles for data submission and access.

## Technologies Used
- **Backend**: Python, Flask, MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL for storing biodiversity data
- **Visualization**: Matplotlib, Plotly for data visualization

## Installation

### Prerequisites
- Python 3.x
- MySQL
- Flask
- pip

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/tejasrajegowda/biodiversity.git
    ```
2. Navigate to the project directory:
    ```bash
    cd biodiversity
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the MySQL database and import the schema from `schema.sql`.
5. Configure the database connection in `config.py`.
6. Run the Flask application:
    ```bash
    python app.py
    ```

## Usage
- After installation, the app can be accessed via `http://localhost:5000`.
- Users can log in, manage biodiversity data, and visualize trends.

## Future Enhancements
- Add machine learning models for biodiversity predictions.
- Include support for real-time data streaming from IoT devices.
- Expand visualizations with additional graph types and metrics.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
