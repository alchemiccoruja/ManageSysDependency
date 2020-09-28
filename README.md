# ManageSysDependency

This is simple implementation of apt-get (or application installer).
It take as inout a file contains INSTALL, REMOVE, DEPEND, LIST, and END commands.

INSTALL: Install the package(s).
DEPEND: Specify a package followed by the other packages it depends
REMOVE: Uninstall a package(s)
LIST: List the install packages.

----------------------How to Run----------------------
1) git clone https://github.com/alchemiccoruja/ManageSysDependency.git

2) cd ManageSysDependency/ManageSysDependency

3) python  sys_dependency_mini_app.py /full/path/to/input.txt
