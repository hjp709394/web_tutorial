# virtual environment
sudo apt-get install python-pip
pip install virtualenv
virtualenv -p /usr/bin/python2 ./env

source ./env/bin/activate

# install required packages
pip install flask Jinja2 flask-restful
