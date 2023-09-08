from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

VERSION = '0.1.0'
DESCRIPTION = 'A simple TOTP MFA CLI authenticator'

# Setting up
setup(
    name="mfa",
    version=VERSION,
    license="GPLv3",
    author="JustScott",
    author_email="<development@scottwyman.me>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url = "https://github.com/JustScott/mfa",
    project_urls={
        "Bug Reports":"https://github.com/JustScott/mfa/issues",
    },
    package_dir={"":"src"},
    packages=["mfa"],
    install_requires=["keyring>=24.2.0","typer<=0.9.0", "pyotp>=2.8.0", "psutil>=5.9.5"],
    keywords=['python','security','mfa', '2fa'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.0',
        'Topic :: Security :: Cryptography'
    ]
)

