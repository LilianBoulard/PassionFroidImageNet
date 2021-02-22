# PassionFroidImageNet (PFIN)
Repository for the Ynov 48h challenge


## Technical information

This project uses a NoSQL database to store images.

Two configuration variables are defined:
- `PFIN_SERVER`: the server's address.  
- `PFIN_SECRET`: a secret key used locally.

Both are set in the file `pfin/config.py`.


## Cloning the repository locally

    git clone https://github.com/LilianBoulard/PassionFroidImageNet


## Installing the requirements

The web server runs Python, and requires some additional packages.  
Those are listed in the file `requirements.txt`.

To install them, launch the command:

    pip install -r requirements.txt


## Launching the server

Finally, to launch the server, use the command

    python app.py
