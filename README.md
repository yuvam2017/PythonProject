# Chat Application Using Python
## Requirement
	1. Python (__version__ >= 3.5)
	2. Kivy
	3. Socket 
	4. Time (Module)
## Details
Ayush Pratap Singh – CSC/20/47 <br>
D R Yuvam – CSC/20/48 <br>
### Modules Used: <br>
 Socket- For networking. <br>
 Threading- For multi-tasking <br>
 Kivy- Kivy is a platform independent GUI framework for python. <br>

### Project Structure:
The project contains two standalone python files, one for the client and one for
the server. For the client side file to run, user must make sure that kivy is installed
via pip (pip install –upgrade pip) and the server is up and running with the correct
connection details written in the client file. To keep the project simple, we opted
to run the server on localhost and expose a port on our machine to allow other
people on the internet establish a socket connection and hence use the chat
application through a secure tunnel. This project will also be available for android
devices as kivy’s buildozer utility allows us to compile any kivy project to android
or ios package.
