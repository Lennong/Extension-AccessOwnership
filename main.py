#
# AccessOwnership post-processing script for NZBGet
#

import os
import sys
import re

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_ERROR=94

# Check if all required script config options are present in config file
required_options = ('NZBPO_DESTDIR', 'NZBPO_ACCESS', 'NZBPO_OWNER', 'NZBPO_GROUP')
for optname in required_options:
    if (not optname in os.environ):
        print('[ERROR] Option %s is missing in configuration file. Please check script settings' % optname[6:])
        sys.exit(POSTPROCESS_ERROR)

# Add variables for added categories
categories = []
for i in range(1, 100):
    catextname = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_NAME")
    catextdir = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_DESTDIR")
    catextaccess = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_ACCESS")
    catextowner = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_OWNER")
    catextgroup = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_GROUP")
    if catextname == None or catextdir == None:
        break
    categories.append({catextname, catextdir, catextaccess, catextowner, catextgroup})

# Init script options with values from NZBGet configuration file
category = os.environ['NZBPP_CATEGORY'];
nzbname = os.environ['NZBPP_NZBNAME'];
destdir = os.environ['NZBPO_DESTDIR'];
access = os.environ['NZBPO_ACCESS'];
owner = os.environ['NZBPO_OWNER'];
group = os.environ['NZBPO_GROUP'];

# If download is an added category, set the related destination dir
if not category == "":
    for i in range(1, 100):
        if os.environ.get("NZBPO_CategoryExt" + str(i) + ".Name") is not None:
            if category == os.environ.get("NZBPO_CategoryExt" + str(i) + ".Name"):
                destdir = os.environ["NZBPO_CategoryExt" + str(i) + ".DestDir"];
                access = os.environ["NZBPO_CategoryExt" + str(i) + ".Access"];
                owner = os.environ["NZBPO_CategoryExt" + str(i) + ".Owner"];
                group = os.environ["NZBPO_CategoryExt" + str(i) + ".Group"];

# Check if input values contains positive integers only
if not re.match('^[0-9]*$', access):
    print("Category",category,": Invalid Access[octal] settings:",[access],"Use positive integers only!")
    sys.exit(POSTPROCESS_ERROR)
if not re.match('^[0-9]*$', owner):
    print("Category",category,": Invalid Owner[UID] settings:",[owner],"Use positive integers only!")
    sys.exit(POSTPROCESS_ERROR)
if not re.match('^[0-9]*$', group):
    print("Category",category,": Invalid Group[GID] settings:",[group],"Use positive integers only!")
    sys.exit(POSTPROCESS_ERROR)

# Apply chmod & chown to files in destination dir
if os.path.exists(os.path.join(destdir, nzbname)):
    print(category,": Modifying access permissions & ownership on",nzbname)
    os.chmod(os.path.join(destdir, nzbname), int(access, base=8))
    for root,dirs,files in os.walk(os.path.join(destdir, nzbname)):
        for d in dirs :
            os.chmod(os.path.join(root,d), int(access, base=8))
        for f in files :
            os.chmod(os.path.join(root,f), int(access, base=8))
    os.chown(os.path.join(destdir, nzbname), int(owner), int(group))
    for root,dirs,files in os.walk(os.path.join(destdir, nzbname)):
        for d in dirs :
            os.chown(os.path.join(root,d), int(owner), int(group))
        for f in files :
            os.chown(os.path.join(root,f), int(owner), int(group))

sys.exit(POSTPROCESS_SUCCESS)
