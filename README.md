# Skyhook
Send and recieve files securely through the IPFS network

# Overview
Skyhook is a command-line tool that allows the user to securely share files over the IPFS network.
It features:
-   Seamless file encryption and decryption using AES-256
-   Local history of file names, hashes, keys and dates which can be both imported and exported easily
-   Ability to run off both local and remote IPFS nodes

# Usage
Simply running Skyhook with no arguments gives the user a list of available commands:

```
    skyhook clear history   -   Delete everything from history
    skyhook list history    -   List all entries in history
    skyhook list keys       -   List all files and their corresponding encryption keys
    
    skyhook search [comma-separated list of file names and/or hashes]  -   Search history for entries matching [file names and/or hashes]
    skyhook delete [comma-separated list of file names and/or hashes]  -   Delete entries specified by [file names and/or hashes] from history
    skyhook save [comma-separated list of file names and/or hashes]    -   Save history entries specified by [file names and/or hashes] to the current directory
    
    skyhook import [comma-separated list of paths]   -   Import history from a location specified by [paths]
    skyhook export [path]   -   Export entire history to a location specified by [path]
    
    skyhook upload [comma-separated list of file names]  -   Upload a file specified by [file names] from the current directory to the IPFS network
    skyhook download [comma-separated list of hashes]    -   Download a file specified by [hashes] from the IPFS network to the current directory

```

# Requirements
The only requirements for running Skyhook are the ipfs-api and skyhookfilecrypt modules for Python 3, which can be installed by running:

```
pip3 install ipfs-api skyhookfilecrypt
```

or

```
pip3 install --user ipfs-api skyhookfilecrypt
```
# Other versions
Skyhook for Windows can be found here: https://github.com/deedeecx330/skyhook-windows
