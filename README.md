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

## Basic CLI usage

```bash
mfa add Apple P5UH5YH4WVYVSMXV # Add a new seed
mfa show Apple # Show a single code
mfa show-all # Show all codes
mfa show-seed Apple # Show a single seed
mfa delete Apple # Delete from seed file

mfa lock # Lock the seed file (removes the decryption key from the keyring)
mfa auto-lock 2 # Starts a background script to lock the seed file every 2 minutes

mfa export-seeds --no-encrypt # Print all seeds unencrypted to stdout
mfa export-seeds > file.aes # Put all seeds encrypted to a file
mfa import-seeds file.aes # Import those seeds on another machine

# Change the seed file path and auto lock interval in the config file directly
mfa config-settings --seed-file-path "/home/user" --auto-lock-interval 6
mfa export-config > config.json # Export your configurations
mfa import-config config.json
```

## Basic programmatic usage
```python3
>>> from mfa import mfa
>>> mfa.add(name="Meta", seed="P5UH5TH4XYYVSMXV")
>>> mfa.show("Meta")
'569242'
>>> mfa.show_all()
Enter the seed file's decryption key:
{'Apple': '448273', 'Meta': '001084'}
>>> mfa.show_seed("Apple")
'P5UH5YH4WVYVSMXV'
>>> mfa.export_seeds(encrypt=False)
{'Apple': 'P5UH5YH4WVYVSMXV', 'Meta': 'P5UH5TH4XYYVSMXV'}
# Can only import seeds from file, may change in the future
>>> mfa.import_seeds("seed_file_path.aes")
>>> mfa.lock() # True if successfuly locked
True
>>> mfa.auto_lock(5) # Change the auto-locking interval to 5 minutes
5
>>> mfa.config_settings(seed_file_path="/home/user/secrets_dir", auto_lock_interval=6)
Moving /home/user/mfa_secrets.aes to /home/user/secret_dir
{'auto_lock_interval': 6, 'seed_file_path': '/home/administrator/secret_dir'}
>>> mfa.export_config()
{'auto_lock_interval': 6, 'seed_file_path': '/home/user/secret_dir'}
>>> mfa.export_config(export_file_path="exported_config.json")
True
>>> mfa.import_config(file_path="exported_config.json")
True
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

python3 -m unittest discover ../../unittests/ "*_tests.py" # Run all unittests
```

