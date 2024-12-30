# Banking System Project

## Description
This project is a simple Banking System application built with Python and MySQL. It allows users to manage accounts, perform transactions, and update their profiles. The system includes functionalities such as account creation, user login, credit/debit transactions, balance inquiry, and fund transfers.

## Features
- **User Management**:
  - Add new users with validations for email, contact number, and password.
  - View all registered users.
  - Update user profiles.
- **Transaction Management**:
  - Credit and debit transactions.
  - Fund transfer between accounts.
  - Maintain transaction history.
- **Account Security**:
  - Password validation ensures strong passwords.
  - Login system with password protection.
- **Database Integration**:
  - Uses MySQL to store user and transaction details.
  - Relational tables for `users` and `transactions`.

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python libraries:
  - `mysql-connector-python`

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd banking-system
   ```

2. **Install Dependencies**:
   ```bash
   pip install mysql-connector-python
   ```

3. **Setup MySQL**:
   - Ensure MySQL Server is installed and running.
   - Update MySQL credentials (`host`, `user`, `password`) in the script as per your configuration.

4. **Run the Application**:
   ```bash
   python <script-name>.py
   ```

## Tables and Schema

### Users Table
- `id`: Auto-increment primary key
- `name`: User's name
- `account_number`: Unique 10-digit account number
- `dob`: Date of birth
- `city`: City of residence
- `password`: User's password
- `balance`: Account balance
- `contact_number`: User's contact number
- `email_id`: User's email address
- `address`: User's physical address
- `is_active`: Account active status (default: TRUE)

### Transactions Table
- `id`: Auto-increment primary key
- `account_number`: Account involved in the transaction (foreign key)
- `type`: Transaction type (e.g., Credit, Debit, Transfer In, Transfer Out)
- `amount`: Transaction amount
- `date`: Timestamp of the transaction

## Usage

1. **Add a User**:
   - Provide the required details such as name, date of birth, city, contact, email, etc.
   - The system generates a unique account number and validates input.

2. **Login**:
   - Use account number and password to log in.

3. **Perform Transactions**:
   - Check balance, credit, debit, or transfer funds.

4. **Update Profile**:
   - Update user details like name, city, email, and address.

5. **View Users** (Admin functionality):
   - View all registered users and their details.

## Validation Rules

- **Password**: At least 8 characters, includes uppercase letters and digits.
- **Email**: Valid email format.
- **Contact Number**: Exactly 10 digits.
- **Initial Balance**: Minimum of 2000.

## Notes
- Ensure that MySQL Server is running before executing the script.
- Change the MySQL connection credentials if required.
- Default password in the script: `1234` (modify for production environments).

## Future Enhancements
- Add an admin panel for better user management.
- Include encryption for password storage.
- Add a graphical user interface (GUI).

## License
This project is for educational purposes and does not include any licensing terms. Feel free to modify and expand it as needed.

---

Enjoy managing your banking operations with this Python-powered system!

