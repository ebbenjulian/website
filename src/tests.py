from database import main
from bcrypt import hashpw, gensalt, checkpw


def run_test():
    print("Running tests...")

    username = "testuser"
    email = "testuser@example.com"
    password = "testpass"

    success, result, error = main.fetch_one(
        "SELECT userid, username, password_hash FROM users WHERE username = ?",
        (username,)
    )

    if not success:
        print(f"Database error while checking user: {error}")
        return

    if result:
        print("User already exists, checking password...")

        # Works whether result is a dict or tuple/list
        stored_hash = (
            result["password_hash"]
            if isinstance(result, dict)
            else result[2]
        )

        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")

        if checkpw(password.encode("utf-8"), stored_hash):
            print("User exists and password matches.")
        else:
            print("User exists but password does not match.")

        return

    print("User does not exist, creating user...")

    hashed_password = hashpw(
        password.encode("utf-8"),
        gensalt()
    ).decode("utf-8")

    success, error = main.execute(
        """
        INSERT INTO users 
        (username, email, password_hash, role, created_at, last_login)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, NULL)
        """,
        (username, email, hashed_password, "user")
    )

    if not success:
        print(f"Failed to create user: {error}")
        return

    print("User created successfully.")


if __name__ == "__main__":
    run_test()