# Ignition - The StartASM Interpreter

## Overview
Ignition is StartASM's own interpreter and runtime virtual machine for code testing and debugging. It's an extension of the StartASM language specification, and requires the base compiler as a dependency. Fully implemented in Python, Ignition is ready to launch any StartASM program!

## Usage
Before starting, make sure you have a local binary of a StartASM compiler on your machine. This project also requires Python version 3.6 or greater. Once installed on your local machine, download the repository and navigate into the root directory.

While in the directory, run the following command to build the module locally:
```bash
pip install .
```
After that, Ignition should be ready to start. 

On first run, the program will ask for a path to a local StartASM compiler instance. Simply enter the location of the compiler on your machine. 
```bash
Please enter the full path to your C++ binary: {Your StartASM Compiler Path Here}
```

After that, the interpreter can be started by simply executing:
```bash
ignition start
```

This will begin the interpreter loop, which the `--help` command can provide furhter usage information for. To terminate an ignition instance, simply run `end`.

As of right now, Ignition has very little real functionality aside from is interface, but futher implementation will be added gradually over time.

## License
This project is licensed under the MIT license. Feel free to fork or contribute to this project or use it in any manner you like.