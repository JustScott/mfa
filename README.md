# MFA

A simple TOTP MFA CLI Authenticator


### Security

MFA uses pythons built-in cryptography library to encrypt your file
with all your seed phrases (refered to as "seed file" in the project)
with 256 bit AES in CBC mode. 

Your password is hashed using the pbkdf2 algorithm with sha256 and
500,000 iterations. You set your password the first time you interact
with the mfa tool and it should stay in your native keychain from there on.

### Features

My goal with this project is to keep both the code and the CLI options
as simple and minimal as possible.

```bash
# Commands:
add             # Add a new entry to your seed file
delete          # Delete an entry from your seed file
show            # Show a single name and generated TOTP code
show-all        # Show all the names and generated TOTP codes
show-seed       # Get a seed phrase from your seed file
export-seeds    # Export the seed file content to a file (mfa_export.aes)
import-seeds    # Import a previously exported file, overwriting the existing seeds
lock            # Lock the seed file, AKA remove the password from the keyring
auto-lock       # Start a background script that runs the lock command at user set intervals
config-settings # Change any setting in the config file
export-config   # Export the json config to a file or stdout
import-config   # Import a previously exported json config file
```


## Development

( The `keyrings.alt` pypi package is used for testing only )

### Setting up the environment

```python3
python3 -m venv venv # Create the virtual environment

# Activate the virtual environment in the current terminal
source venv/bin/activate 

pip install -r requirements.txt # Install the required dependencies
```

### Running the application
```python3
cd src/mfa

python3 mfa.py
```

### Running unittests

```python3
cd src/mfa # Moving to this directory to call the tests is important

python3 ../../tests/mfa_tests.py # Run tests on mfa.py only
#or
bash ../../run_all_tests.sh # Run tests on all
```

