# Ignition - The StartASM Interpreter

## Overview
Ignition is StartASM's own interpreter and runtime virtual machine for code testing and debugging. It's an extension of the StartASM language specification, and requires the base compiler as a dependency. Fully implemented in Python, Ignition is ready to launch any StartASM program!

## Usage
Before starting, make sure you have a local docker image of a StartASM compiler on your machine. Note the name given during the build phase - by default, it should be called `startasm` (If you followed the README installation guide).
Then, while in the `Ignition` directory, run the following command to build the module locally:
```
pip install .
```
After that, Ignition should be ready to start. 

On first run, the program will ask for the docker image name of your StartASM Compiler. Simply enter the name used during `docker build`. For example:
```
Please enter the full name of your StartASM Docker Image: startasm
```

After that, the interpreter can be started by simply executing:
```
ignition start
```

This will begin the interpreter loop, which the `--help` command can provide further usage information for. To terminate an ignition instance, simply run `end`.

As of right now, Ignition has very little real functionality aside from is interface, but further implementation will be added gradually over time.

## License
This project is licensed under the MIT license. Feel free to fork or contribute to this project or use it in any manner you like.