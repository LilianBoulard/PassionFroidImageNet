# PassionFroidImageNet
Repository for the Ynov 48h challenge


## Technical information

This project uses a NoSQL database and stores images .  

Note: due to privacy concerns, the server's address is not hard-coded, 
but referenced by the environment variable `PFIN_SERVER`.

It uses Flask for the front-end, which uses another environment variable named `PFIM_SECRET`.


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
