import logging
import time
import re
import json
import urllib3
import requests
LOGGER = logging.getLogger()


def set_data(data):
    global test
    test = data


def delete_fileset(test_data):
    """
    Deletes the primaryFset provided in configuration file
    if primaryFset not deleted , asserts

    Args:
        param1: test_data : contents of configuration file

    Returns:
       None

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    unlink_fileset(test_data)
    delete_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/" + \
        test_data["primaryFs"]+"/filesets/"+test_data["primaryFset"]
    response = requests.delete(
        delete_link, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    time.sleep(10)
    get_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["primaryFs"]+"/filesets/"
    response = requests.get(get_link, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    search_format = '"'+test_data["primaryFset"]+'",'
    search_result = re.search(search_format, str(response.text))
    LOGGER.debug(search_result)
    if search_result is None:
        LOGGER.info(
            f'Success : Fileset {test_data["primaryFset"]} has been deleted')
    else:
        LOGGER.error(
            f'Failed : Fileset {test_data["primaryFset"]} has not been deleted')
        LOGGER.error(get_link)
        LOGGER.error(response.text)
        assert False


def unlink_fileset(test_data):
    """
    unlink primaryFset provided in configuration file

    Args:
        param1: test_data : contents of configuration file

    Returns:
       None

    Raises:
       None

    """
    time.sleep(10)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    unlink_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/" + \
        test_data["primaryFs"]+"/filesets/"+test_data["primaryFset"]+"/link"
    response = requests.delete(
        unlink_link, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    LOGGER.info(f'Fileset {test_data["primaryFset"]} unlinked')
    time.sleep(10)


def fileset_exists(test_data):
    """

    Checks primaryFset provided in configuration file exists or not

    Args:
        param1: test_data : contents of configuration file

    Returns:
       returns True , if primaryFset exists
       returns False , if primaryFset does not exists

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["primaryFs"]+"/filesets/"
    time.sleep(10)
    response = requests.get(get_link, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    search_format = '"'+test_data["primaryFset"]+'",'
    search_result = re.search(search_format, str(response.text))
    if search_result is None:
        return False
    return True


def cred_check(test_data):
    """
    checks if given parameters in test_data are correct
    by calling API using that data

    if API gives any error , It asserts
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/cluster"
    try:
        response = requests.get(get_link, verify=False, auth=(test_data["username"], test_data["password"]))
        LOGGER.debug(response.text)
    except:
        LOGGER.error(f'not able to use Scale REST API , Check cr file (guiHost = {test_data["guiHost"]})')
        assert False

    if not(response.status_code == 200):
        LOGGER.error("API response is ")
        LOGGER.error(str(response))
        LOGGER.error("not able to use scale REST API")
        LOGGER.error("Recheck parameters of config/test.config file")
        LOGGER.error(f'must check username and password for {test_data["guiHost"]}')
        assert False


def link_fileset(test_data):
    """
    link primaryFset provided in configuration file

    Args:
        param1: test_data : contents of configuration file

    Returns:
       None

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    fileset_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/" + \
        test_data["primaryFs"]+"/filesets/"+test_data["primaryFset"]+"/link"
    response = requests.post(fileset_link, verify=False,
                             auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    LOGGER.info(f'Fileset {test_data["primaryFset"]} linked')
    time.sleep(5)


def create_fileset(test_data):
    """
    create primaryFset provided in configuration file

    Args:
        param1: test_data : contents of configuration file

    Returns:
       None

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["primaryFs"]+"/"
    time.sleep(2)
    response = requests.get(get_link, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    response_dict = json.loads(response.text)
    scalehostpath = response_dict["filesystems"][0]["mount"]["mountPoint"]
    create_fileset_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["primaryFs"]+"/filesets"
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }
    data = '{"filesetName":"'+test_data["primaryFset"]+'","path":"' + \
        scalehostpath+'/'+test_data["primaryFset"]+'"}'

    response = requests.post(create_fileset_link, headers=headers,
                             data=data, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    LOGGER.info(f'Fileset {test_data["primaryFset"]} created and linked')
    time.sleep(5)


def unmount_fs(test_data):
    """
    unmount primaryFs provided in configuration file

    Args:
        param1: test_data : contents of configuration file

    Returns:
       None

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    unmount_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["primaryFs"]+"/unmount"
    LOGGER.debug(unmount_link)
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }
    data = '{"nodes":["'+test_data["guiHost"]+'"],"force": false}'
    response = requests.put(unmount_link, headers=headers,
                            data=data, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    time.sleep(5)

    get_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["primaryFs"]
    response = requests.get(get_link, verify=False, auth=(test_data["username"], test_data["password"]))
    response_dict = json.loads(response.text)
    mounted_on = response_dict["filesystems"][0]["mount"]["nodesMountedReadWrite"]

    if test_data["guiHost"] in mounted_on:
        LOGGER.error(f'Unable to unmount {test_data["primaryFs"]} from {test_data["guiHost"]}')
        assert False

    LOGGER.info(f'primaryFS {test_data["primaryFs"]} unmounted from {test_data["guiHost"]}')


def mount_fs(test_data):
    """
    mount primaryFs provided in configuration file

    Args:
        param1: test_data : contents of configuration file

    Returns:
       None

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    mount_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["primaryFs"]+"/mount"
    LOGGER.debug(mount_link)
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }
    data = '{"nodes":["'+test_data["guiHost"]+'"]}'
    response = requests.put(mount_link, headers=headers,
                            data=data, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)
    time.sleep(5)

    get_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["primaryFs"]
    response = requests.get(get_link, verify=False, auth=(test_data["username"], test_data["password"]))
    response_dict = json.loads(response.text)
    mounted_on = response_dict["filesystems"][0]["mount"]["nodesMountedReadWrite"]

    if test_data["guiHost"] not in mounted_on:
        LOGGER.error(f'Unable to mount {test_data["primaryFs"]} on {test_data["guiHost"]}')
        assert False
    LOGGER.info(f'primaryFS {test_data["primaryFs"]} mounted on {test_data["guiHost"]}')


def cleanup():
    """
    deletes all primaryFsets that matches pattern pvc-
    used for cleanup in case of parallel pvc.

    Args:
       None

    Returns:
       None

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_link = "https://"+test["guiHost"]+":"+test["port"] + \
        "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/"
    response = requests.get(get_link, verify=False, auth=(test["username"], test["password"]))
    lst = re.findall(r'\S+pvc-\S+', response.text)
    lst2 = []
    for la in lst:
        lst2.append(la[1:-2])
    for res in lst2:
        volume_name = res
        unlink_link = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/" + \
            test["primaryFs"]+"/filesets/"+volume_name+"/link"
        response = requests.delete(
            unlink_link, verify=False, auth=(test["username"], test["password"]))
        LOGGER.debug(response.text)
        LOGGER.info(f"Fileset {volume_name} unlinked")
        time.sleep(5)
        delete_link = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/" + \
            test["primaryFs"]+"/filesets/"+volume_name
        response = requests.delete(
            delete_link, verify=False, auth=(test["username"], test["password"]))
        LOGGER.debug(response.text)
        time.sleep(10)
        get_link = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/"
        response = requests.get(get_link, verify=False,
                                auth=(test["username"], test["password"]))
        LOGGER.debug(response.text)
        search_result = re.search(volume_name, str(response.text))
        if search_result is None:
            LOGGER.info(f'Fileset {volume_name} deleted successfully')
        else:
            LOGGER.error(f'Fileset {volume_name} is not deleted')
            assert False


def delete_created_fileset(volume_name):
    """
    deletes primaryFset created by pvc

    Args:
        param1: volume_name : fileset to be deleted

    Returns:
       None

    Raises:
       None

    """
    if volume_name is None:
        return
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_link = "https://"+test["guiHost"]+":"+test["port"] + \
        "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/"
    response = requests.get(get_link, verify=False, auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)
    search_result = re.search(volume_name, str(response.text))
    LOGGER.debug(search_result)
    if search_result is None:
        LOGGER.info(f'Fileset Delete : Fileset {volume_name} has already been deleted')
    else:
        unlink_link = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/" + \
            test["primaryFs"]+"/filesets/"+volume_name+"/link"
        response = requests.delete(
            unlink_link, verify=False, auth=(test["username"], test["password"]))
        LOGGER.debug(response.text)
        LOGGER.info(f'Fileset {volume_name} has been unlinked')
        time.sleep(5)
        delete_link = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/" + \
            test["primaryFs"]+"/filesets/"+volume_name
        response = requests.delete(
            delete_link, verify=False, auth=(test["username"], test["password"]))
        LOGGER.debug(response.text)

        for _ in range(0, 12):
            get_link = "https://"+test["guiHost"]+":"+test["port"] + \
                "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/"
            response = requests.get(get_link, verify=False,
                                    auth=(test["username"], test["password"]))
            LOGGER.debug(response.text)
            search_result = re.search(volume_name, str(response.text))
            LOGGER.debug(search_result)
            if search_result is None:
                LOGGER.info(f'Fileset Delete : Fileset {volume_name} has been deleted successfully')
                return
            time.sleep(15)
            LOGGER.info(f'Fileset Check : Checking for Fileset {volume_name}')
        LOGGER.error(f'Fileset Delete : Fileset {volume_name} deletion operation failed')
        assert False


def created_fileset_exists(volume_name):
    """
    Checks fileset volume_name exists or not

    Args:
        param1: volume_name : fileset to be checked

    Returns:
       returns True , if volume_name exists
       returns False , if volume_name does not exists

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_link = "https://"+test["guiHost"]+":"+test["port"] + \
        "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/"
    time.sleep(10)
    response = requests.get(get_link, verify=False, auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)
    search_format = '"'+volume_name+'",'
    search_result = re.search(search_format, str(response.text))
    if search_result is None:
        return False
    return True


def create_dir(dir_name):
    """
    creates directory named dir_name

    Args:
       param1: dir_name : name of directory to be created

    Returns:
       None

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    dir_link = "https://"+test["guiHost"]+":"+test["port"] + \
        "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/directory/"+dir_name
    LOGGER.debug(dir_link)
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }
    data = '{ "user":"' + test["uid_name"]+'", "uid":'+test["uid_number"] + \
        ', "group":"'+test["gid_name"]+'", "gid":' + test["gid_number"]+' }'
    response = requests.post(dir_link, headers=headers,
                             data=data, verify=False, auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)
    LOGGER.info(f'Directory Create : Creating directory {dir_name}')
    check_dir(dir_name)


def check_dir(dir_name):
    """
    checks directory dir_name is present or not
    asserts  if not present
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    val = 0
    while val < 12:
        check_dir_link = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/owner/"+dir_name
        LOGGER.debug(check_dir_link)
        headers = {
            'accept': 'application/json',
        }
        response = requests.get(check_dir_link, headers=headers,
                                verify=False, auth=(test["username"], test["password"]))
        LOGGER.debug(response.text)
        if response.status_code == 200:
            LOGGER.info(f'Directory Check : directory {dir_name} created successfully')
            return
        time.sleep(15)
        LOGGER.info(f'Directory Check : Checking for directory {dir_name}')
        val += 1
    LOGGER.error(f'directory {dir_name} not created successfully')
    LOGGER.error(str(response))
    LOGGER.error(str(response.text))
    assert False


def delete_dir(dir_name):
    """
    deleted directory named dir_name

    Args:
       param1: dir_name : name of directory to be deleted

    Returns:
       None

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    dir_link = "https://"+test["guiHost"]+":"+test["port"] + \
        "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/directory/"+dir_name
    LOGGER.debug(dir_link)
    headers = {
        'content-type': 'application/json',
    }
    response = requests.delete(
        dir_link, headers=headers, verify=False, auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)
    LOGGER.info(f'Deleted directory {dir_name}')
    time.sleep(5)


def get_FSUID():
    """
    return the UID of primaryFs

    Args:
       None

    Returns:
       FSUID

    Raises:
       None

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    info_filesystem = "https://"+test["guiHost"]+":"+test["port"] + \
        "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"?fields=:all:"
    response = requests.get(info_filesystem, verify=False,
                            auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)
    lst = re.findall(r'\S+uuid[\S.\s]+', response.text)
    FSUID = str(lst[0][10:27])
    LOGGER.debug(FSUID)
    return FSUID


def get_mount_point():
    """
    return the mount point of primaryFs

    Args:
       None

    Returns:
       mount point

    Raises:
       None

    """

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if "type_remote" in test:
        info_filesystem = "https://"+test["type_remote"]["guiHost"]+":"+test["type_remote"]["port"] + \
            "/scalemgmt/v2/filesystems/"+test["remoteFs"]+"?fields=:all:"
        response = requests.get(info_filesystem, verify=False,
                                auth=(test["type_remote"]["username"], test["type_remote"]["password"]))
    else:
        info_filesystem = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"?fields=:all:"
        response = requests.get(info_filesystem, verify=False,
                                auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)
    response_dict = json.loads(response.text)
    mount_point = response_dict["filesystems"][0]["mount"]["mountPoint"]
    LOGGER.debug(mount_point)
    return mount_point


def get_remoteFs_remotename(test_data):
    """ return name of remote filesystem's remote name """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    info_filesystem = "https://"+test_data["guiHost"]+":"+test_data["port"] + \
        "/scalemgmt/v2/filesystems/"+test_data["remoteFs"]
    response = requests.get(info_filesystem, verify=False,
                            auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)

    response_dict = json.loads(response.text)
    for filesystem in response_dict["filesystems"]:
        if filesystem["name"] == test_data["remoteFs"]:
            device_name = filesystem["mount"]["remoteDeviceName"]
            LOGGER.debug(device_name)
            temp_split = device_name.split(":")
            return temp_split[1]
    return None


def check_snapshot(snapshot_name, volume_name):
    """
    checks if snapshot is snapshot_name created for volume_name

    if created returns True
    else return False
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    val = 0
    while val < 12:
        snap_link = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/" + \
            volume_name+"/snapshots"
        response = requests.get(snap_link, verify=False,
                                auth=(test["username"], test["password"]))
        LOGGER.debug(response.text)
        LOGGER.info(f"Snapshot Check : Checking for snapshot {snapshot_name} of volume {volume_name}")
        response_dict = json.loads(response.text)
        LOGGER.debug(response_dict)

        for snapshot in response_dict["snapshots"]:
            if snapshot["snapshotName"] == snapshot_name:
                return True
        val += 1
        time.sleep(5)
    return False


def create_snapshot(snapshot_name, volume_name, created_objects):
    """
    create snapshot snapshot_name for volume_name
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }

    data = '{ "snapshotName": "'+snapshot_name+'" }'
    snap_link = "https://"+test["guiHost"]+":"+test["port"] + \
        "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/" + \
        volume_name+"/snapshots"
    response = requests.post(snap_link, headers=headers, data=data, verify=False,
                             auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)
    created_objects["scalesnapshot"].append([snapshot_name, volume_name])
    LOGGER.info(f"Static Snapshot Create :snapshot {snapshot_name} created for volume {volume_name}")


def delete_snapshot(snapshot_name, volume_name, created_objects):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    snap_link = "https://"+test["guiHost"]+":"+test["port"] + \
        "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/" + \
        volume_name+"/snapshots/"+snapshot_name
    response = requests.delete(snap_link, verify=False, auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)
    created_objects["scalesnapshot"].remove([snapshot_name, volume_name])
    LOGGER.info(f"Scale Snapshot Delete :snapshot {snapshot_name} of volume {volume_name} is deleted")


def check_snapshot_deleted(snapshot_name, volume_name):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    val = 0
    while val < 12:
        snap_link = "https://"+test["guiHost"]+":"+test["port"] + \
            "/scalemgmt/v2/filesystems/"+test["primaryFs"]+"/filesets/" + \
            volume_name+"/snapshots"
        response = requests.get(snap_link, verify=False,
                                auth=(test["username"], test["password"]))
        LOGGER.debug(response.text)
        LOGGER.info(f"Snapshot Check : Checking for deletion of snapshot {snapshot_name} of volume {volume_name}")
        response_dict = json.loads(response.text)
        LOGGER.debug(response_dict)

        snapshots_list = []
        for snapshot in response_dict["snapshots"]:
            snapshots_list.append(snapshot["snapshotName"])

        if snapshot_name in snapshots_list:
            val += 1
            time.sleep(10)
        else:
            return True
    return False


def snapshot_available():
    """
    returns True , if snapshot feature is available
    else , returns False
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_link = "https://"+test["guiHost"]+":"+test["port"] + "/scalemgmt/v2/info"
    response = requests.get(get_link, verify=False, auth=(test["username"], test["password"]))
    LOGGER.debug(response.text)

    response_dict = json.loads(response.text)
    LOGGER.info(f'scale version is {response_dict["info"]["serverVersion"]}')
    scale_version = response_dict["info"]["serverVersion"]
    scale_version = scale_version[0] + scale_version[2] + scale_version[4] + scale_version[6]
    if int(scale_version) >= 5110:
        return True
    LOGGER.warning("Snapshot restore feature is not supported")
    return False


def get_scale_version(test_data):
    """
    get spectrum scale version and display it
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_link = "https://"+test_data["guiHost"]+":"+test_data["port"] + "/scalemgmt/v2/info"
    response = requests.get(get_link, verify=False, auth=(test_data["username"], test_data["password"]))
    LOGGER.debug(response.text)

    response_dict = json.loads(response.text)
    LOGGER.info(f'scale version is {response_dict["info"]["serverVersion"]}')
