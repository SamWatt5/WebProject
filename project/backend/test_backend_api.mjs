import fetch from "node-fetch";

const BASE_URL = "http://localhost:8000/api";

// ANSI escape codes for colors
const GREEN = "\x1b[32m";
const RED = "\x1b[31m";
const BLUE = "\x1b[34m";
const RESET = "\x1b[0m";

function printResult(testCase, description, result, expected) {
  if (result === expected) {
    console.log(`${GREEN}[PASS]${RESET} ${testCase}: ${description}`);
  } else {
    console.log(`${RED}[FAIL]${RESET} ${testCase}: ${description}`);
    console.log(`  Expected: ${expected}, Got: ${result}`);
  }
}

async function testSignup() {
  const url = `${BASE_URL}/auth/signup`;
  const payload = {
    fname: "John",
    lname: "Doe",
    email: "john.doe@example.com",
    username: "johndoe",
    password: "Password123",
  };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    printResult("TC-BACK-001", "Verify user signup", response.status, 201);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }
}

async function testLogin() {
  const url = `${BASE_URL}/auth/login`;

  // Valid credentials
  const validPayload = { username: "johndoe", password: "Password123" };
  try {
    const validResponse = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(validPayload),
    });
    printResult("TC-BACK-002", "Login with valid credentials", validResponse.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }

  // Invalid password
  const invalidPasswordPayload = { username: "johndoe", password: "WrongPassword" };
  try {
    const invalidPasswordResponse = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(invalidPasswordPayload),
    });
    printResult("TC-BACK-002", "Login with invalid password", invalidPasswordResponse.status, 401);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }

  // User not found
  const invalidUserPayload = { username: "nonexistentuser", password: "Password123" };
  try {
    const invalidUserResponse = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(invalidUserPayload),
    });
    printResult("TC-BACK-002", "Login with nonexistent user", invalidUserResponse.status, 404);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }
}

async function testAdminPermissions(userId) {
  const url = `${BASE_URL}/admin/permissions/${userId}`;

  // Grant admin privileges
  try {
    const grantResponse = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    printResult("TC-BACK-004", "Grant admin privileges", grantResponse.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }

  // Remove admin privileges
  try {
    const removeResponse = await fetch(url, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });
    printResult("TC-BACK-004", "Remove admin privileges", removeResponse.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }
}

async function testGetAllUsers() {
  const url = `${BASE_URL}/admin/users`;

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    printResult("TC-BACK-005", "Retrieve all user accounts", response.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }
}

async function testUserManagement(username) {
  const url = `${BASE_URL}/admin/users/${username}`;

  // Find user
  try {
    const findResponse = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    printResult("TC-BACK-006", "Find user by username", findResponse.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }

  // Remove user
  try {
    const removeResponse = await fetch(url, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });
    printResult("TC-BACK-006", "Remove user by username", removeResponse.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }
}

async function testUserMe() {
  const url = `${BASE_URL}/user/me`;

  // Retrieve user info
  try {
    const retrieveResponse = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    printResult("TC-BACK-007", "Retrieve user info", retrieveResponse.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }

  // Update user info
  const updatePayload = {
    fname: "Jane",
    lname: "Doe",
    email: "jane.doe@example.com",
    username: "janedoe",
    password: "NewPassword123",
  };
  try {
    const updateResponse = await fetch(url, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatePayload),
    });
    printResult("TC-BACK-007", "Update user info", updateResponse.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }

  // Delete user account
  try {
    const deleteResponse = await fetch(url, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });
    printResult("TC-BACK-007", "Delete user account", deleteResponse.status, 200);
  } catch (error) {
    console.error(`${RED}[ERROR]${RESET} ${error.message}`);
  }
}

async function runTests() {
  console.log(`${BLUE}Running Backend API Tests...${RESET}`);
  await testSignup();
  await new Promise((resolve) => setTimeout(resolve, 1000));
  await testLogin();
  await new Promise((resolve) => setTimeout(resolve, 1000));
  await testAdminPermissions("user-id-placeholder"); // Replace with actual user ID
  await new Promise((resolve) => setTimeout(resolve, 1000));
  await testGetAllUsers();
  await new Promise((resolve) => setTimeout(resolve, 1000));
  await testUserManagement("johndoe");
  await new Promise((resolve) => setTimeout(resolve, 1000));
  await testUserMe();
}

runTests();