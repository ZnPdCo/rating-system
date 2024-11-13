"""
Filename: custom/auto_status.py
Author: ZnPdCo
"""


# Please remove the below line if you need verification of the account credentials.
# pylint: disable=unused-argument
def auto_status(username):
    """
    If you want to use the auto-update feature for the problems that a user has passed or
    attempted, please implement the function `auto_status(username)` in the file
    `app/custom/auto_status.py`. This function should be able to fetch the problems that
    the `username` has passed/attempted.

    This function needs to return a dictionary, similar to:
    ```
    {
        "1": 0,
        "5": 1,
        "7": 0
    }
    ```
    Here, the keys are the problem IDs, and the values indicate whether the problem was passed
    (0 means attempted, 1 means passed). If the user has not submitted a particular problem,
    then that key-value pair should be omitted.

    Note that PID here refers to OJ ones, not this system ones.

    Returns
        A dict of problem status of OJ PID.
    """

    return {}
