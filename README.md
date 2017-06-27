[![Head to Waffle.io](https://img.shields.io/badge/Waffle.io--blue.svg?label=Waffle.io&title=Waffle.io&style=social)](https://waffle.io/JosephMart/Flix-with-Friends) [![Head to Slack](https://img.shields.io/badge/Slack--lightgrey.svg?label=Slack&title=Slack&style=social)](https://return0software.slack.com/messages/general/) [![Python Documentation](https://img.shields.io/badge/python-3.5.2-orange.svg?title=3.5.2&style=flat-square)](https://docs.python.org/release/3.5.2/) [![GTK+ Documentation](https://img.shields.io/badge/GTK%2B-3.22-brightgreen.svg?style=flat-square)](https://developer.gnome.org/gtk3/stable/)

<p align="center">
<a href="https://github.com/Return0Software/Flix-with-Friends"><img src="https://raw.githubusercontent.com/Return0Software/Flix-with-Friends/master/images/FLIX_W_FRIENDS_1.jpg" align="center" height="256" width="256" ></a></p>


# Flix with Friends

Developed by [Joseph Martinsen](https://github.com/JosephMart), [Tristan Partin](https://github.com/tristan957), and [Hudson Birdsong](https://github.com/Hudson35).
Developed on [Solus](https://solus-project.com/) using [Atom](https://atom.io/) and [Visual Studio Code](https://code.visualstudio.com/).

Flix with Friends is a program that helps users decide what movie they should watch. It reads
through spreadsheets or Google Sheets that have names of movies that users would like to watch.
The program searches through a movie database to pull descriptions, ratings and various poster
sizes to present in an IMDb-like interface to help users decide on what movie to watch based on
search criteria like keywords, release date, rating and which of the users has seen the movie.

## How to Use
*(Insert App Usage)*

## How to Install
Currently throwing around ideas which could include a `Makefile` or a `setup.py`. Stay tuned. Dependencies are currently written in `dependencies.txt`. Make sure to install them. Python dependencies should be installed using `pip3`.

As of right now you can clone the repository and run `python3 flix-with-friends` or simply `make`.

## Future Development
Flix with Friends is leveraging the latest Python and GTK+ versions available on Solus. We, the developers will keep it up to date to the best of our ability with

In no particular order:
- [ ] Better File Organization
- [ ] Create Server with RasberryPi
- [ ] Solid State Drive for Storage
- [ ] Implement a Load from Server Button
- [ ] New Movie Box UI as Reveler
- [ ] Fully Implement the Google Doc
- [ ] Create Logo

## Contribution Guide
Steps are the same on any OS. Detailed commands are for developers using Solus.

Install Python3 requirements `pip3 install -r requirements.txt`

Download the latest [VirtualBox Installer](https://www.virtualbox.org/wiki/Linux_Downloads). If in browser, [direct link (5.1.22)](http://download.virtualbox.org/virtualbox/5.1.22/VirtualBox-5.1.22-115126-Linux_amd64.run) right click link and Save As. Now install the dependencies and VirtualBox like so:
```bash
sudo eopkg it -c system.devel
sudo eopkg it linux-lts-headers
sudo sh ~/Downloads/VirtualBox-5.1.22-115126-Linux_amd64.run
```
Replace the version number of the file with the one you downloaded

Install Vagrant
```bash
sudo eopkg install vagrant
```

Navigate to the root of the repo.
```bash
vagrant up # will take time for the first time
vagrant ssh
# TODO database setup and migrations
```

## License
[GPL 2.0](https://github.com/JosephMart/Flix-with-Friends/blob/master/LICENSE)
