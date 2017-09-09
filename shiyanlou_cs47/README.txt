sudo apt-get update
sudo apt-get install python-gtk2 python-webkit python-pip

virtualenv -p python2 env
source env/bin/activate

pip install requests

cd /env/lib/python2.7/
mkdir dist-packages/
cd dist-packages/

ln -s /usr/lib/python2.7/dist-packages/cairo/ 
ln -s /usr/lib/python2.7/dist-packages/pygtk.py
ln -s /usr/lib/python2.7/dist-packages/pygtk.pth 
ln -s /usr/lib/python2.7/dist-packages/gtk-2.0/
ln -s /usr/lib/python2.7/dist-packages/gobject/
ln -s /usr/lib/python2.7/dist-packages/glib/
ln -s /usr/lib/python2.7/dist-packages/webkit/
ln -s /usr/lib/python2.7/dist-packages/gi/
