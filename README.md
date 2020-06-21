# Python-bot to automatically make novel music!

## Steps to get started ##
 1. Clone the repository
 2. Replace the `credentials.json` from the email-id you want the bot to be from google email api generatory [here](https://developers.google.com/gmail/api/quickstart/python). Also complete step 2 & install all the required libraries. 
## Install all the other required libraries ->

Install the required libraries ->	
- **Magenta == 1.1.1**: Some functions used here are depricated in the later versions. This version works without any issues. If you have conda than create a new environment using `conda create --name music python=3.7` *(I prefer python 3.7)* and then activate the same using `conda activate music`. Once that is done you can simply install magenta using -> `pip install magenta==1.1.1`

- **base64**: It should be installed by default. But make sure to still check for the same.
- **urlextract**: Install urlextract using `pip install urlextract`
- **gitPython**: Install using `pip install gitPython`

## Other important things to note
In the `main.py` file, make sure you change the variables such as `dir_to_clone` & `input_file_dir`. Rest everything should work fine!
