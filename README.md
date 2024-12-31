# StartDebugger - The StartASM Interpreter

## Overview
StartDebugger is StartASM's own interpreter and runtime virtual machine for code testing and debugging. It's an extension of the StartASM language specification, and requires the base compiler as a dependency. Fully implemented in Python, StartDebugger is ready to launch any StartASM program!

## Usage
Before starting, make sure you have a local docker image of a StartASM compiler on your machine. Note the name given during the build phase - by default, it should be called `startasm` (If you followed the README installation guide).
Then, while in the `Ignition` directory, run the following commands to build the module locally:
```
pip install -r requirements.txt
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

As of right now, StartDebugger can interpret very basic StartASM programs, and more functionality will be added soon.

## License
This project is licensed under the MIT license. Feel free to fork or contribute to this project or use it in any manner you like.
