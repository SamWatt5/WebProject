import requests
import time  # Import the time module for sleep

BASE_URL = "http://localhost:8000/api" 

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Global variable to store user information
USER_DICT = None


def print_result(test_case, description, result, expected):
    """
    Prints the test result in color-coded format using ANSI escape codes.
    """
    if result == expected:
        print(f"{GREEN}[PASS]{RESET} {test_case}: {description}")
    else:
        print(f"{RED}[FAIL]{RESET} {test_case}: {description}")
        print(f"  Expected: {expected}, Got: {result}")


# Helper function to retrieve the user dictionary
def get_user_info(username):
    global USER_DICT
    url = f"{BASE_URL}/auth/test-user-id"
    payload = {"username": username}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        USER_DICT = response.json().get("user")
        print(f"{BLUE}User dictionary retrieved: {USER_DICT}{RESET}")
    else:
        print(f"{RED}[FAIL]{RESET} Failed to retrieve user info. Status code: {response.status_code}")
        print(f"Response: {response.text}")


# TC-BACK-001: Verify that a new user can be created with valid data
def test_signup():
    url = f"{BASE_URL}/auth/signup"
    payload = {
        "fname": "John",
        "lname": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "Password123"
    }
    response = requests.post(url, json=payload)
    print_result("TC-BACK-001", "Verify user signup", response.status_code, 201)


# TC-BACK-002: Test login with valid and invalid credentials
def test_login():
    url = f"{BASE_URL}/auth/login"

    # Valid credentials
    valid_payload = {"username": "johndoe", "password": "Password123"}
    valid_response = requests.post(url, json=valid_payload)
    print_result("TC-BACK-002", "Login with valid credentials", valid_response.status_code, 200)

    # Invalid password
    invalid_password_payload = {"username": "johndoe", "password": "WrongPassword"}
    invalid_password_response = requests.post(url, json=invalid_password_payload)
    print_result("TC-BACK-002", "Login with invalid password", invalid_password_response.status_code, 401)

    # User not found
    invalid_user_payload = {"username": "nonexistentuser", "password": "Password123"}
    invalid_user_response = requests.post(url, json=invalid_user_payload)
    print_result("TC-BACK-002", "Login with nonexistent user", invalid_user_response.status_code, 404)


# TC-BACK-004: Test granting and removing admin privileges
def test_admin_permissions():
    global USER_DICT
    if not USER_DICT:
        print(f"{RED}[FAIL]{RESET} TC-BACK-004: User dictionary not found. Run test_signup and get_user_info first.")
        return

    user_id = USER_DICT["_id"]
    url = f"{BASE_URL}/admin/permissions/{user_id}"

    # Grant admin privileges
    grant_response = requests.post(url, json={"user": USER_DICT})
    print_result("TC-BACK-004", "Grant admin privileges", grant_response.status_code, 200)

    # Remove admin privileges
    remove_response = requests.delete(url, json={"user": USER_DICT})
    print_result("TC-BACK-004", "Remove admin privileges", remove_response.status_code, 200)


# TC-BACK-005: Verify all user accounts can be retrieved
def test_get_all_users():
    url = f"{BASE_URL}/admin/users"
    response = requests.get(url)
    print_result("TC-BACK-005", "Retrieve all user accounts", response.status_code, 200)


# TC-BACK-006: Verify that an individual user can be found and removed
def test_user_management():
    global USER_DICT
    if not USER_DICT:
        print(f"{RED}[FAIL]{RESET} TC-BACK-006: User dictionary not found. Run test_signup first.")
        return

    user_id = USER_DICT["_id"]
    url = f"{BASE_URL}/admin/users/{user_id}"

    # Find user
    find_response = requests.get(url)
    print_result("TC-BACK-006", "Find user by ID", find_response.status_code, 200)

    # Remove user
    remove_response = requests.delete(url)
    print_result("TC-BACK-006", "Remove user by ID", remove_response.status_code, 200)


# TC-BACK-007: Verify user info retrieval, update, and deletion
def test_user_me():
    url = f"{BASE_URL}/user/me"

    # Retrieve user info
    retrieve_response = requests.get(url)
    print_result("TC-BACK-007", "Retrieve user info", retrieve_response.status_code, 200)

    # Update user info
    update_payload = {
        "fname": "Jane",
        "lname": "Doe",
        "email": "jane.doe@example.com",
        "username": "janedoe",
        "password": "NewPassword123"
    }
    update_response = requests.patch(url, json=update_payload)
    print_result("TC-BACK-007", "Update user info", update_response.status_code, 200)

    # Delete user account       
    delete_response = requests.delete(url)
    print_result("TC-BACK-007", "Delete user account", delete_response.status_code, 200)


# Add sleep between test functions
if __name__ == "__main__":
    print(f"{BLUE}Running Backend API Tests...{RESET}")
    test_signup()
    time.sleep(1)  # Add a 1-second delay
    get_user_info("johndoe")  # Retrieve the user dictionary for the test user
    time.sleep(1)  # Add a 1-second delay
    test_login()
    time.sleep(1)  # Add a 1-second delay
    test_admin_permissions()
    time.sleep(1)  # Add a 1-second delay
    test_get_all_users()
    time.sleep(1)  # Add a 1-second delay
    test_user_management()
    time.sleep(1)  # Add a 1-second delay
    test_user_me()