import os

# IPFS node host
# Example:
# host = "https://ipfs.infura.io"

# IPFS node port
# Example:
# port = 5001

# Temporary directory where all the processing happens
tmpDir = "/tmp"

# Skyhook directory
skyhookDir = "{}/.local".format(os.environ["HOME"])

# History location
dbLocation = "{}/skyhook.db".format(skyhookDir)

# Configuration file location
configFile = "{}/skyhook.config".format(skyhookDir)
