from uuid import UUID

def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid("c9bf9e57-1685-4c89-bafb-ff5af830be8a")
    True
    >>> is_valid_uuid("c9bf9e58")
    False
    """
    # Taken from https://stackoverflow.com/a/33245493
    try:
        UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return True

def is_version_id(id):
    """
    Checks if the provided value is a valid version identifier.
    """

    version_id_parts = id.split("::")
    if id is not None and isinstance(id, str):
        if len(version_id_parts) == 3:
            if is_valid_uuid(version_id_parts[0]):
                if version_id_parts[2].isdecimal():
                    return True
    return False

def is_versioned_object_id(id):
    """
    Checks if the provided value is a valid versioned object identifier.
    """

    if id is not None and isinstance(id, str):
        version_id_parts = id.split("::")
        if len(version_id_parts) == 1:
            if is_valid_uuid(version_id_parts[0]):
                return True
    return False

def extract_versioned_object_id_from_version_id(version_id):
    """
    Extracts the versioned object identifier from the identifier of one of its versions.
    """

    version_id_parts = version_id.split("::")

    versioned_object_id = version_id_parts[0]

    return versioned_object_id
