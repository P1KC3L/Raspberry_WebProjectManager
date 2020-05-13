# Raspberry Web Project Manager

This repository hands off a local web application that stores a dashboard with some projects that can be controlled remotely with a Raspberry board. 

Currently, this application has just one project, that was made to set up and control remotely some RGB leds connected to the Raspberry GPIOs. 

To run the aplication, please follow the next instructions:

1- Open a terminal in the folder in which you will download the repository and clone it using the git command:
```
git clone https://github.com/P1KC3L/Raspberry_WebProjectManager.git
```
2- Next, get the app running by executing the ```launcher.sh``` file:
```
./Raspberry_WebProjectManager/launcher.sh
```
3- Finally, to use the application, open your browser and search _localhost:5000_

The page will display a link to go to the home project management page, where a button for the RGB lights will be displayed.
Once inside the page of the RGB lights controller, add a RGB led by typing the GPIO pins of the Raspberry where the led was connected.

(Note: I suggest using the the pins 18, 13, 12 / 23, 19, 18 as they count with PWM.)
