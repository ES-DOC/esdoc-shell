Introduction
------------------------------

The esdoc-shell is the command line interface between a system admin / developer / user and the ES-DOC software stack.  The shell supports 20+ commands and uses a few config files which are installed along with the stack.

Installing
------------------------------

**Step 1: Download source code from GitHub**

```
git clone https://github.com/ES-DOC/esdoc-shell.git YOUR_WORKING_DIRECTORY/esdoc
```

**Step 2: Run installer**

```
source YOUR_WORKING_DIRECTORY/esdoc/activate && esdoc-stack-install
```

This downloads the full ES-DOC stack source code, creates a local python executable, creates a local virtual environment, creates local configuration files.  It takes approx. 10 minutes to execute.

**Step 3: Review installation**

Explore the install directory, i.e. YOUR_WORKING_DIRECTORY/esdoc.  The ops sub-directory contains local resources created during the lifetime of the shell, this includes config files and logs.

**Step 4: Activation**

Remember to add the following line to your bash profile file ($HOME/.bash_profile):

```
source YOUR_WORKING_DIRECTORY/esdoc/activate
```

Remember to start a new bash session.

Updating
------------------------------

```
esdoc-stack-update-source
```

Execute this command regularly to ensure that the shell and associated repos are upto date.

Uninstalling
------------------------------

```
esdoc-stack-uninstall
```

Usage
------------------------------

Usage instructions: `<https://github.com/ES-DOC/esdoc-shell/blob/master/docs/usage.rst>`
