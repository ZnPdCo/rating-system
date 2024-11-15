"""
Filename: custom/auto_problems.py
Author: ZnPdCo
"""

# pylint: disable=unused-import
from app.admin.api import add_problem


# Please remove the below line if you need verification of the account credentials.
# pylint: disable=unused-argument
def auto_problems(params):
    """
    If you want to use the auto-update feature for the problems, please implement the
    function `auto_problem(params)` in the file `app/custom/auto_problems.py`. This
    function should be able to fetch the problems through the params.

    You can use `add_problem(contest, name, info)` function from the `app/admin/api.py`
    file to add the problems to the database.
    """
