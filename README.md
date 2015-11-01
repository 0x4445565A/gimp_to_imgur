# Gimp to Imgur export

This is a tool written in Python that allows users to easily export images to Imgur.

Installation
-------------
To install this plugin you can do a variety of things but I have set up two "install paths"...

To install WITH revisions and git support you simply git clone the repo then create a symbolic link to the gimp plugins directory.
<pre>
cd ~/.gimp-2.8
mkdir plug-ins #create the dir incase it doesn't exist
ssh clone git@github.com:tehbmar/gimp_to_imgur.git
ls -s gimp_to_imgur/export_to_imgur.py .
chmod +x export_to_imgur.py
</pre>

To install WITHOUT git support run the following.
<pre>
cd ~/.gimp-2.8
mkdir plug-ins #create the dir incase it doesn't exist
wget https://raw.githubusercontent.com/tehbmar/gimp_to_imgur/master/export_to_imgur.py
chmod +x export_to_imgur.py
</pre>


Running the Plugin
-------------
To export your image from GIMP to Imgur navigate to File > Export to Imgur

The plugin will then open your Imgur link in a new window in your browser.
