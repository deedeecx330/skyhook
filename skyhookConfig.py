import os

# IPFS Host
# Example:
# host = "/dns/ipfs.infura.io/tcp/5001/https"

# Temporary directory for file processing
tmpDir = "/tmp"

# Skyhook directory
skyhookDir = "{}/.local/skyhook".format(os.environ["HOME"])
