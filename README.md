# L 4 Logic
> Design circuits of logic elements!

See **[wiki pages](https://github.com/archy-co/l4logic/wiki)** for complete description and documentation.

![Contributors](https://img.shields.io/github/contributors/archy-co/l4logic)
![License](https://img.shields.io/github/license/archy-co/l4logic)
![Languages](https://img.shields.io/github/languages/top/archy-co/l4logic)
![Issues](https://img.shields.io/github/issues-closed/archy-co/l4logic)

## Table of content

* [Getting Started](#getting-started)
    * [Install](#install)
    * [Uninstall](#uninstall)
* [Usage](#usage)
* [Demo](#demo)
* [Authors](#authors)

## Getting Started
### Install
You can install `l4logic` in two ways:
* locally, in the project folder (this method uses `venv` under the hood)
* system wide, installing all dependencies globally on your system and adding executable file
to system path.

This program is tested to work on Linux. As MacOS is also unix-based system, this program
will probably run properly on Mac. Windows is not officially supported and you may have troubles
installing the program on Windows. In any case, you can install dependencies manually 
(they are listed in [`requirements.txt`](https://github.com/archy-co/l4logic/blob/main/requirements.txt)), and run l4logic with command `python main.py`.

In any case, to run the application, you should have `python` installed. Official supported version for python: 3.8, but should work on earlier 3.x versions as well as with 3.8+ versions.

#### Local installation
First you need to clone repository and go to it. Then run `make install` to create virtual
environment, install dependencies into virtual environment and create executable shell file
that runs the program. Here's all the command you need to use:

```shell
$ git clone https://github.com/archy-co/l4logic.git
$ cd l4logic
$ make install
```

#### Global Installation
Global installation varies a bit from local installation: first of all, all dependencies will be
installed on system wide; secondly, virtual environment will not be used. The commands to install
globally are the same except the last line
```shell
$ git clone https://github.com/archy-co/l4logic.git
$ cd l4logic
$ make install_globally
```
NOTE: This command requires root privileges to copy executable to path (so that you can
launch application from wherever)

### Uninstall
To uninstall the program using make, run

```shell
$ make uninstall
```

in project folder.

NOTE: This command requires root privileges to delete executable file `l4logic` from system path
(if you previously installed program system wide), but can be run without root rights.

See `make help` for more information on possible commands

## Usage

After **[installation](#installation)**, launch the program running `l4logic` (if you have it
installed system wide) or `./l4logic` from current directory (if it is installed locally)

The user have to use specific set of commands to be able to interact with program.

These commands includes `add`, `del` for elements and `>`, `!>` for connection.

For adding a new element user should use command as follows:

`add *element_type* *id(name)* *cor1* *cor2*`, where `cor1` and `cor2` are **x** and **y** coordinates accordingly.

Examples:

    add and 0 20 20
    add or 1 3 4

---

For deleting existing element user should use command as follows:
`del *id(name)*`

Examples:

    del 0
    del 1

---

For adding new connection between elements user should use next command:

`*id1(name)* *output_label1* > *id2(name)* *input_label1*`

Example:

    0 out > 1 in1

---

For deleting existing connection between elements user should use next command:

`*id1(name)* *output_label1* !> *id2(name)* *input_label1*`

Example:

    0 out !> 1 in1

For full documentation, project description and more information on usage see **[wiki pages](https://github.com/archy-co/l4logic/wiki)**

## Demo
You can try load example files like [examples/4bit_ALU.txt](https://github.com/archy-co/l4logic/blob/master/images/demo.gif). To do so just insert path to example file in program's input field and click **Load**

Here is a short gif that shows some basic commands and functionality

![screen-gif](./images/demo.gif)

## License
L 4 Logic is licensed under the MIT license. See **[LICENSE](https://github.com/archy-co/l4logic/blob/master/LICENSE)** for more information.


## Authors
* Bohdan Mahometa
* Viktor Povazhuk
* Maksym Tsapiv
* Bohdan Ivashko
* Yaroslav Revera

