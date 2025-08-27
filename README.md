# Employee Management System

This project is a Flask-based **Employee Management System** designed to help administrators efficiently manage employee details. The system allows admins to perform CRUD (Create, Read, Update, Delete) operations on employee records and includes a secure login system. A simple dark theme provides a modern user interface.

***

### Features

-   **Authentication**: Secure user login and logout functionality.
-   **User Management**: Only admins can create new user accounts.
-   **Employee Management**: Admins can add, edit, view, and delete employee records.
-   **Search Functionality**: Easily search for employees by their name or email.
-   **Pagination**: The employee list is paginated for better navigation and performance.

***

### Technologies Used

-   **Backend**: Python with Flask
-   **Frontend**: HTML, CSS, Jinja2
-   **Database**: SQLite

***

### How to Run the Project

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment:**

    *For Windows:*
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
    *For macOS/Linux:*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

5.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000`.

***

### How to Use

On the first run, a default admin account is automatically created. Use the following credentials to log in:

-   **Username**: `admin`
-   **Password**: `admin123`

Once logged in, the admin can view the employee list, add new employees, edit details, delete records, and create other user accounts via the **Create User** option.
