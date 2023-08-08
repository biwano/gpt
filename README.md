# Installation

pdf2text requires poppler. For install to install poppler on Rockylinux
sudo dnf install -y https://mirrors.oit.uci.edu/rocky-linux/8/devel/x86_64/os/Packages/p/poppler-cpp-20.11.0-6.el8.x86_64.rpm
sudo dnf install -y https://mirrors.oit.uci.edu/rocky-linux/8/devel/x86_64/os/Packages/p/poppler-devel-20.11.0-6.el8.x86_64.rpm
sudo dnf install -y https://mirrors.oit.uci.edu/rocky-linux/8/devel/x86_64/os/Packages/p/poppler-cpp-devel-20.11.0-6.el8.x86_64.rpm

Then install dependencies

`pip install -r requirements.txt`

- in a .env file put values for
``` 
OPENAI_API_KEY
PINECONE_API_KEY
```

- create some directories
```
mkdir -p var/pdfs/pending
mkdir -p var/pdfs/processed
```

# PDFS

## Process a PDF file

Put some pdfs in `var/pdfs/pending`

`./cli.sh pdf process var/pdfs/pending/*`

## Restore a PDF file

`./cli.sh pdf restore var/pdfs/processed/*`

# Ask the bot a question

`./cli.sh process-pdf process-pdf var/pdfs/pending/*`

# Run the chat app

`flask run --host 0.0.0.0`



