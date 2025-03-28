import requests
import time  # Import the time module for sleep
import json  # Import json for pretty-printing

BASE_URL = "http://localhost:8000/api"

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Global variables to store user information
USER_DICT = None  # Authenticated admin user
NEW_USER_DICT = None  # Newly created non-admin user

# Create a session object to persist cookies
session = requests.Session()


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
    global USER_DICT, NEW_USER_DICT
    url = f"{BASE_URL}/auth/test-user-id"
    payload = {"username": username}
    response = session.post(url, json=payload)  # Use the session object
    if response.status_code == 200:
        user = response.json().get("user")
        if username == "johndoe":
            USER_DICT = user
        elif username == "janedoe":
            NEW_USER_DICT = user
        print(f"{BLUE}User dictionary retrieved for {username}:{RESET}")
        print(json.dumps(user, indent=4))  # Pretty-print the user dictionary
    else:
        print(f"{RED}[FAIL]{RESET} Failed to retrieve user info for {username}. Status code: {response.status_code}")
        print(f"Response: {response.text}")


# TC-BACK-001: Verify that a new user can be created with valid data
def test_signup(username, email):
    url = f"{BASE_URL}/auth/signup"
    payload = {
        "fname": "Test",
        "lname": "User",
        "email": email,
        "username": username,
        "password": "Password123"
    }
    response = requests.post(url, json=payload)  # Use a new session for the new user
    print_result("TC-BACK-001", f"Verify user signup for {username}", response.status_code, 201)
    if response.status_code == 201:
        return True
    return False


# TC-BACK-004: Test granting admin privileges using the test endpoint
def make_admin():
    if not USER_DICT:
        print(f"{RED}[FAIL]{RESET} TC-BACK-004: User dictionary not found. Run test_signup and get_user_info first.")
        return

    url = f"{BASE_URL}/admin/test-grant-admin/{USER_DICT['_id']}"
    response = session.post(url)  # Use the session object
    print_result("TESTCALL", "Grant admin privileges to authenticated user", response.status_code, 200)


# TC-BACK-004: Test granting admin privileges to the new user
def test_grant_admin():
    if not NEW_USER_DICT:
        print(f"{RED}[FAIL]{RESET} TC-BACK-004: New user dictionary not found. Run create_user and get_user_info first.")
        return

    url = f"{BASE_URL}/admin/permissions/{NEW_USER_DICT['_id']}"
    response = session.post(url, headers={"Content-Type": "application/json"})  # Use the session object
    print_result("TC-BACK-004", f"Grant admin privileges to user {NEW_USER_DICT['username']}", response.status_code, 200)


# TC-BACK-004: Test removing admin privileges from the new user
def test_remove_admin():
    if not NEW_USER_DICT:
        print(f"{RED}[FAIL]{RESET} TC-BACK-004: New user dictionary not found. Run create_user and get_user_info first.")
        return

    url = f"{BASE_URL}/admin/permissions/{NEW_USER_DICT['_id']}"
    response = session.delete(url, headers={"Content-Type": "application/json"})  # Use the session object
    print_result("TC-BACK-004", f"Remove admin privileges from user {NEW_USER_DICT['username']}", response.status_code, 200)


# TC-BACK-005: Verify all user accounts can be retrieved
def test_get_all_users():
    url = f"{BASE_URL}/admin/users"
    response = session.get(url, headers={"Content-Type": "application/json"})  # Use the session object
    print_result("TC-BACK-005", "Retrieve all user accounts", response.status_code, 200)
    if response.status_code == 200:
        print(f"{BLUE}All users:{RESET}")
        print(json.dumps(response.json(), indent=4))  # Pretty-print the list of users


# TC-BACK-006: Verify that an individual user can be found and removed
def test_user_management(username):
    url = f"{BASE_URL}/admin/users/{username}"

    # Find user
    response = session.get(url, headers={"Content-Type": "application/json"})  # Use the session object
    print_result("TC-BACK-006", f"Find user {username}", response.status_code, 200)
    if response.status_code == 200:
        print(f"{BLUE}User details for {username}:{RESET}")
        print(json.dumps(response.json(), indent=4))  # Pretty-print the user details

    # Remove user
    response = session.delete(url, headers={"Content-Type": "application/json"})  # Use the session object
    print_result("TC-BACK-006", f"Remove user {username}", response.status_code, 200)


# TC-BACK-007: Verify that the user's info can be retrieved, updated, and deleted
def test_user_me():
    url = f"{BASE_URL}/user/me"

    # Retrieve user info
    response = session.get(url, headers={"Content-Type": "application/json"})  # Use the session object
    print_result("TC-BACK-007", "Retrieve authenticated user's info", response.status_code, 200)
    if response.status_code == 200:
        print(f"{BLUE}Authenticated user's info:{RESET}")
        print(json.dumps(response.json(), indent=4))  # Pretty-print the user's info

    # Update user info
    update_payload = {
        "fname": "Updated",
        "lname": "User",
        "email": "updated.email@example.com",
        "username": "updatedjohndoe",
        "password": "NewPassword123"
    }
    response = session.patch(url, json=update_payload, headers={"Content-Type": "application/json"})  # Use the session object
    print_result("TC-BACK-007", "Update authenticated user's info", response.status_code, 200)

    # Delete user account
    response = session.delete(url, headers={"Content-Type": "application/json"})  # Use the session object
    print_result("TC-BACK-007", "Delete authenticated user's account", response.status_code, 200)


# Add sleep between test functions
if __name__ == "__main__":
    print(f"{BLUE}Running Backend API Tests...{RESET}")

    # Step 1: Create the admin user (johndoe)
    test_signup("johndoe", "john.doe@example.com")
    time.sleep(1)   

    # Step 2: Retrieve the admin user's info
    get_user_info("johndoe")
    time.sleep(1)   

    # Step 3: Log in as the admin user
    url = f"{BASE_URL}/auth/login"
    payload = {"username": "johndoe", "password": "Password123"}
    response = session.post(url, json=payload)
    print_result("TC-BACK-002", "Login as admin user", response.status_code, 200)
    time.sleep(1)   

    # Step 4: Grant admin privileges to the admin user
    make_admin()
    time.sleep(1)   

    # Step 5: Create the test user (janedoe)
    test_signup("janedoe", "jane.doe@example.com")
    time.sleep(1)   

    # Step 6: Retrieve the test user's info
    get_user_info("janedoe")
    time.sleep(1)   

    # Step 7: Grant admin privileges to the test user
    test_grant_admin()
    time.sleep(1)   

    # Step 8: Remove admin privileges from the test user
    test_remove_admin()
    time.sleep(1)   

    # Step 9: Retrieve all user accounts
    test_get_all_users()
    time.sleep(1)   

    # Step 10: Manage the test user (find and remove)
    test_user_management("janedoe")
    time.sleep(1)   

    # Step 11: Manage the authenticated admin user (retrieve, update, delete)
    test_user_me()
