# Computer Vision Web Scaffold
A scaffold for deploying dockerized flask applications.

If you have any questions, feel free to open an issue on [Github](https://github.com/organization-x/omni/issues).

### Video Guide
[![Deploy a Web Project with Flask](https://img.youtube.com/vi/JUb-PpejA7w/0.jpg)](https://youtu.be/JUb-PpejA7w "Deploy a Web Project with Flask")

This guide covers how you can quickly deploy most projects with the [Flask](https://flask.palletsprojects.com/) framework and our omni scaffold.

### Quickstart Guide for Local Development

First clone this repository through 

`https://github.com/organization-x/omni`

cd into the `/app` folder

`python3 -m pip install -r requirements.txt`

edit line 29 the `main.py` file to either the URL of the cocalc server you are on or `localhost` if you are running it on your own PC

Then, clone ultralytics yolov5 in the app folder, by running 

`git clone https://github.com/ultralytics/yolov5`
`pip install -r yolov5/requirements.txt`

Run

 `python3 -m main`

to start the server on local, most changes while developing will be picked up in realtime by the server

### File Structure
The files/directories which you will need to edit are **bolded**

**DO NOT TOUCH OTHER FILES. THIS MAY RESULT IN YOUR PROJECT BEING UNABLE TO RUN**

- .gitignore
- READMD.md
- app/
     - **main.py**
     - **best.pt** <- you will need to upload this yourself after cloning the repo when developing the site
     - **requirements.txt**
     - **utils.py**
     - templates/
          - **index.html**

### How to upload best.pt to your file structure?
Run 
`cp ../path/to/best.pt best.pt`
### best.pt ###
The weights file - must upload if you are running file on coding center or are trying to deploy.
### main.py ###
Contains the main flask app itself.
### requirements.txt ###
Contains list of packages and modules required to run the flask app. Edit only if you are using additional packages that need to be pip installed in order to run the project.

To generate a requirements.txt file you can run

`pip list --format=freeze > app/requirements.txt`

the requirements.txt file will then be updated. Keep in mind: some packages you install on one operating system may not be available on another. You will have to debug and resolve this yourself if this is the case.
### static/ ###
Contains the static images, CSS, & JS files used by the flask app for the webpage. You will need to create this and put files in it. Place all your images used for your website in static/images/ so that you can then reference them in your html files.
### utils.py ###
Contains common functions used by the flask app. Put things here that are used more than once in the flask app.
### templates/ ###
Contains the HTML pages used for the webpage. Edit these to fit your project. index.html is the demo page.