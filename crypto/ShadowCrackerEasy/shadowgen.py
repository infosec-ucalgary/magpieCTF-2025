import crypt
import random
import string

# Function to generate a SHA-512 hash for a password with a random salt
def generate_hash(password):
    # Generate a random salt (16 characters of letters and digits)
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    # Create the hash using SHA-512
    hashed_password = crypt.crypt(password, "$6$" + salt)
    return hashed_password

# Function to process the users.txt and append hashed passwords to them
def hash_passwords_for_users(users_file, password, output_file):
    # Open the users.txt file and the output file
    with open(users_file, 'r') as users, open(output_file, 'w') as output:
        for username in users:
            username = username.strip()  # Remove any extra whitespace or newline
            if username:
                # Generate the hashed password
                hashed_password = generate_hash(password)
                # Write the shadow format line to the output file
                shadow_line = f"{username}:{hashed_password}:18089:0:99999:7:::\n"
                output.write(shadow_line)
                print(f"Processed {username}")  # Optional: to show progress

# Main function to execute the script
if __name__ == "__main__":
    # Input file containing usernames and the desired password
    users_file = "users.txt"
    password = "password123"  # You can change this password if needed
    output_file = "shadow_output.txt"  # The output file that will be written

    # Call the function to process the users
    hash_passwords_for_users(users_file, password, output_file)

    print(f"Hashed passwords have been written to {output_file}.")
