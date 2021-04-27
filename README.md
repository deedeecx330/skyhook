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
    
    skyhook search [file name/hash]  -   Search history for entries matching [file name/hash]
    skyhook delete [file name/hash]  -   Delete entries specified by [file name/hash] from history
    skyhook save [file name/hash]    -   Save history entries specified by [file name/hash] to the current directory
    skyhook add [name:hash:key]      -   Manually add an entry to history specified by colon-separated values of [name:hash:key]
    
    skyhook import [path]   -   Import history from a location specified by [path]
    skyhook export [path]   -   Export entire history to a location specified by [path]
    
    skyhook upload [file name]  -   Upload a file specified by [file name] from the current directory to the IPFS network
    skyhook download [hash]     -   Download a file specified by [hash] from the IPFS network to the current directory	

    It is possible to specify multiple values in a form of a comma-separated list for search,delete,save,import,upload,download and add functions.
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
