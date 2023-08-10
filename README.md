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
add          # Add a new entry to your seed file
delete       # Delete an entry from your seed file
show         # Show a single name and generated TOTP code
show-all     # Show all the names and generated TOTP codes
show-seed    # Get a seed phrase from your seed file
export-seeds # Export the seed file content to a file (mfa_export.aes)
import-seeds # Import a previously exported file, overwriting the existing seeds
lock         # Lock the seed file, AKA remove the password from the keyring
auto-lock    # Start a background script that runs the lock command at user set intervals
```
