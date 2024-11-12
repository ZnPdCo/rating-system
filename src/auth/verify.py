"""
Filename: auth/verify.py
Author: ZnPdCo
"""


# Please remove the below line if you need verification of the account credentials.
# pylint: disable=unused-argument
def verify_account(username, code):
    """
    If you wish to deploy this system, please write the `verify_account(username, code)` function 
    within `src/auth/verify.py` yourself to implement user verification for your Online Judge. 
    You need to make this function crawl description of `username` (or other relevant information) 
    from the OJ and check if the description starts with the `code`. If it does, return `True`; 
    otherwise, return `False`.

    Returns:
        True if the description of `username` starts with the `code`, False otherwise.
    """
    # Example implementation:
    description = code + " welcome to use Rating System!"
    if description.startswith(code):
        return True
    return False
