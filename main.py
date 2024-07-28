#
# AccessOwnership post-processing script for NZBGet
#

import os
import sys
import re
import pwd
import grp

# Exit codes used by NZBGet
POSTPROCESS_SUCCESS=93
POSTPROCESS_ERROR=94

# Check if all required script config options are present in config file
required_options = ('NZBPO_DESTDIR', 'NZBPO_ACCESS', 'NZBPO_OWNER', 'NZBPO_GROUP')
for optname in required_options:
    if (not optname in os.environ):
        print('[ERROR] Option %s is missing in configuration file. Please check script settings' % optname[6:])
        sys.exit(POSTPROCESS_ERROR)

# Check if the script is executed from settings page with a custom command
command = os.environ.get("NZBCP_COMMAND")
test_mode = command == "Test"
if command != None and not test_mode:
    print('[ERROR] Invalid command ' + command)
    sys.exit(COMMAND_ERROR)

# Counters for added Categories
countCategory = 1
for i in range(1, 100):
    if os.environ.get("NZBOP_Category" + str(i) + ".Name") is not None:
        countCategory +=1
countCategoryExt = 1
for i in range(1, 100):
    if os.environ.get("NZBPO_CategoryExt" + str(i) + ".Name") is not None:
        countCategoryExt +=1


if test_mode:
    if not os.environ.get("NZBPO_DestDir") == os.environ.get("NZBOP_DestDir"):
        print("Default Category: Invalid Path:",[os.environ.get("NZBPO_DestDir")])
        check = POSTPROCESS_ERROR
    if not re.match('^[0-7]*$', os.environ.get("NZBPO_Access")):
        print("Default Category: Invalid Access[mask]:",[os.environ.get("NZBPO_Access")])
        check = POSTPROCESS_ERROR

    if not re.match('^[0-9]*$', os.environ.get("NZBPO_Owner")):
        print("Default Category: Invalid Owner[UID]:",[os.environ.get("NZBPO_Owner")],"Use positive integers only!")
        check = POSTPROCESS_ERROR
    else:
        try:
            pwd.getpwuid(int(os.environ.get("NZBPO_Owner")))
        except KeyError:
            print("Default Category: Invalid Owner[UID]:",[os.environ.get("NZBPO_Owner")],"User not in system.")
            check = POSTPROCESS_ERROR

    if not re.match('^[0-9]*$', os.environ.get("NZBPO_Group")):
        print("Default Category: Invalid Group[GID]:",[os.environ.get("NZBPO_Group")],"Use positive integers only!")
        check = POSTPROCESS_ERROR
    else:
        try:
            grp.getgrgid(int(os.environ.get("NZBPO_Group")))
        except KeyError:
            print("Default Category: Invalid Group[UID]: Group[UID]",[os.environ.get("NZBPO_Group")],"Group not in system.")
            check = POSTPROCESS_ERROR

    for i in range(1, countCategoryExt):
            catextname = os.environ["NZBPO_CategoryExt" + str(i) + ".Name"];
            catextdestdir = os.environ["NZBPO_CategoryExt" + str(i) + ".DestDir"];
            catextaccess = os.environ["NZBPO_CategoryExt" + str(i) + ".Access"];
            catextowner = os.environ["NZBPO_CategoryExt" + str(i) + ".Owner"];
            catextgroup = os.environ["NZBPO_CategoryExt" + str(i) + ".Group"];
            if not re.match('^[0-7]*$', catextaccess):
                print(catextname,"Category: Invalid Access[mask]:",[catextaccess])
                check = POSTPROCESS_ERROR

            if not re.match('^[0-9]*$', catextowner):
                print(catextname,"Category: Invalid Owner[UID]:",[catextowner],"Use positive integers only!")
                check = POSTPROCESS_ERROR
            else:
                try:
                    pwd.getpwuid(int(catextowner))
                except KeyError:
                    print(catextname,"Category: Invalid Owner[UID]:",[catextowner],"User not in system!")
                    check = POSTPROCESS_ERROR

            if not re.match('^[0-9]*$', catextgroup):
                print(catextname,"Category: Invalid Group[UID]:",[catextgroup],"Use positive integers only!")
                check = POSTPROCESS_ERROR
            else:
                try:
                    grp.getgrgid(int(catextgroup))
                except KeyError:
                    print(catextname,"Category: Invalid Group[UID]:",[catextgroup],"Group not in system!")
                    check = POSTPROCESS_ERROR
 
            countCategoryName = 1
            for i in range(1, countCategory):
                if catextname == os.environ.get("NZBOP_Category" + str(i) + ".Name") is not None:
                    if not catextdestdir == os.environ.get("NZBOP_Category" + str(i) + ".DestDir"):
                        print(catextname,"Category: Invalid Path:",[catextdestdir])
                        check = POSTPROCESS_ERROR
                else:
                    countCategoryName +=1
                    if countCategoryName >= countCategoryExt:
                        print(catextname,"Category: Invalid CategoryExt Name:",[catextname],"Name not same as in CATEGORIES")   
                        check = POSTPROCESS_ERROR

    try:
        check
    except NameError: 
        sys.exit(POSTPROCESS_SUCCESS)
    else:
        sys.exit(check)


# Add variables for added categories
categories = []
for i in range(1, 100):
    catextname = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_NAME")
    catextdestdir = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_DESTDIR")
    catextaccess = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_ACCESS")
    catextowner = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_OWNER")
    catextgroup = os.environ.get("NZBPO_CATEGORYEXT" + str(i) + "_GROUP")
    if catextname == None or catextdestdir == None:
        break
    categories.append({catextname, catextdestdir, catextaccess, catextowner, catextgroup})


# Init script options with values from NZBGet configuration file
category = os.environ['NZBPP_CATEGORY'];
nzbname = os.environ['NZBPP_NZBNAME'];
destdir = os.environ['NZBPO_DESTDIR'];
access = os.environ['NZBPO_ACCESS'];
owner = os.environ['NZBPO_OWNER'];
group = os.environ['NZBPO_GROUP'];


# If download is an added category, set the related destination dir
if not category == "":
    for i in range(1, countCategoryExt):
        #if os.environ.get("NZBPO_CategoryExt" + str(i) + ".Name") is not None:
            if category == os.environ.get("NZBPO_CategoryExt" + str(i) + ".Name"):
                destdir = os.environ["NZBPO_CategoryExt" + str(i) + ".DestDir"];
                access = os.environ["NZBPO_CategoryExt" + str(i) + ".Access"];
                owner = os.environ["NZBPO_CategoryExt" + str(i) + ".Owner"];
                group = os.environ["NZBPO_CategoryExt" + str(i) + ".Group"];


# Check if input values are valid
if not re.match('^[0-7]*$', access):
    print(category,"Category: Invalid Access[mask]:",[access])
    sys.exit(POSTPROCESS_ERROR)

if not re.match('^[0-9]*$', owner):
    print(category,"Category: Invalid Owner[UID]:",[owner],"Use positive integers only!")
    sys.exit(POSTPROCESS_ERROR)
else:
    try:
        pwd.getpwuid(int(owner))
    except KeyError:
        print(category,"Category: Invalid Owner[UID]:",[owner],"User not in system!")
        sys.exit(POSTPROCESS_ERROR)

if not re.match('^[0-9]*$', group):
    print(category,"Category: Invalid Group[UID]:",[group],"Use positive integers only!")
    sys.exit(POSTPROCESS_ERROR)
else:
    try:
        grp.getgrgid(int(group))
    except KeyError:
        print(category,"Category: Invalid Group[UID]:",[group],"Group not in system!")
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
