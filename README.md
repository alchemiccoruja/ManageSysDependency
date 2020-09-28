# ManageSysDependency

This is a simple implementation of apt-get (or application installer/uninstaller).
It take as input a file contains INSTALL, REMOVE, DEPEND, LIST, and END commands; and executes the commands

1) INSTALL: Install the package(s).
2) DEPEND: Specify a package followed by the other packages it depends.
3) REMOVE: Uninstall a package(s).
4) LIST: List the install packages.
5) END: End of input file.

----------------------How to Run----------------------
1) git clone https://github.com/alchemiccoruja/ManageSysDependency.git

2) cd ManageSysDependency/ManageSysDependency

3) python  sys_dependency_mini_app.py /full/path/to/input.txt
