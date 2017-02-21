## Synopsis

arpi intends to the give the visually impaired a simplified computer experience.


## Motivation

The computer experience can be overwhelming for elderly people
in particular
if their vision is impaired.
To solve the problem we create a very simple user interface,
the input is reduced to six keys (arrows, enter, escape)
and all the text gets read back to the user using text-to-speech.
Furthermore we ensure that the contrast and the font size are appropriate.
The ultimate goal is to run arpi on an RaspberryPI.

![](docs/res/screenshot-arpi.jpeg)


## Installation

     $ pip3 install gTTS newspaper3k
     $ apt-get install libttspico-utils python3-pyqt5 python3-pyqt5.qtquick
     $ git clone https://github.com/ReSqAr/arpi.git
     $ cd arpi
     $ mkdir -p ~/.config/arpi/
     $ cp docs/res/config.ini.template ~/.config/arpi/config.ini
     $ python3 -m arpi

## Apps

There currently three apps.

### Phonebook

Easily save and locate telephone numbers on the computer.

### Photos

Select a galllery folder in `config.ini`,
all subfolders are treated as galleries.

### EMail

Read emails from an IMAP server,
the login details are configued via `config.ini`.


## Contributors

The journey just started, so now is the right time to join!
We are interested in all kinds of contributions,
code, ideas and experiences.

## License

Released under the [GPL3 license](https://opensource.org/licenses/GPL-3.0).

