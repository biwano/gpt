pdf2text requires poppler. For Rockylinux
sudo dnf install -y https://mirrors.oit.uci.edu/rocky-linux/8/devel/x86_64/os/Packages/p/poppler-cpp-20.11.0-6.el8.x86_64.rpm
sudo dnf install -y https://mirrors.oit.uci.edu/rocky-linux/8/devel/x86_64/os/Packages/p/poppler-devel-20.11.0-6.el8.x86_64.rpm
sudo dnf install -y https://mirrors.oit.uci.edu/rocky-linux/8/devel/x86_64/os/Packages/p/poppler-cpp-devel-20.11.0-6.el8.x86_64.rpm

Create embeddings for all text files

ls var/texts/* | xargs -L 1 -d '\n' python cli.py embedding create