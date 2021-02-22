# PassionFroidImageNet (PFIN)
Repository for the Ynov 48h challenge


## Technical information

This project uses a NoSQL database to store images's information.  
They, however, are not directly stored there, but on another host, 
where they are gathered via HTTP requests.

Four configuration variables are defined:
- `PFIN_SERVER` - the server's address.  
- `PFIN_SECRET` - a secret key used locally.
- `SALT` - A salt value used for password hashing.
- `IMAGE_HOST_URL` - The URL of the server hosting the actual images.

They are set in the file `pfin/config.py`.


## Cloning the repository locally

    git clone https://github.com/LilianBoulard/PassionFroidImageNet


## Installing the requirements

The web server runs Python, and requires some additional packages.  
Those are listed in the file `requirements.txt`.

To install them, launch the command:

    pip install -r requirements.txt

*Using a virtual environment is recommended.*

## Launching the server

Finally, to launch the server, simply use the command

    python app.py
