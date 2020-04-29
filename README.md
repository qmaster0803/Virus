**Virus simulator by qmaster0803**
==============================
Hi there! Self-isolation, self-isolation...

Too boring~~

I came up with this idea (at night, of course) ^w^

This program is easy-to-setup and configurable. With it, you can create your own "virus" and watch how it works.

If you can't use it on your PC, you can create an Issue with simulation parameters and I will render simulation for you :)
***
### Setup and requirements

Firstly, you need Python >= 3.7 (I prefer 3.8.1)
You can install it from official site: [Here](https://www.python.org/)

After it, you need some modules for python: opencv and matplotlib
* On Windows: open cmd.exe, type ```py -m pip install opencv-python matplotlib```
* On UNIX: open terminal, type ```sudo apt install python3-pip
```, after ```pip3 install opencv-python matplotlib```

Download .zip archive with project, unpack it to any **empty** folder and double-click on virus_sim.py
***
### What does it look like

There are two graphs: in the upper graph you can see points where people are shown, in the lower graph there are a lot of statistics.

What do the colors mean?
* Blue - healthy man
* Red - infected man
* Green - immunited man
* Black - dead man

What can I customize?
* Speed of moving
* Starting population
* Dimensions of field
* Infect radius
* Chance of infection
* Chance of death
* Illness time
* Birth rate
* Max limit of days
* Self-isolation (come soon)
* Hospitalization (come soon)
