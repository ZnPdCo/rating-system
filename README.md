# Rating System

A concise, easy-to-configure, and powerful algorithm competition problems rating system. Developed with Python and Flask.

You can add problems to the system, rate your algorithm competition problems, or use other people's evaluations to filter problems.

## Help

Improve our translation. In `app/i18n`.

## Screenshots

![](screenshots.png)

## Installation

Please install Python 3.10 or higher, Node.js 18.20 or higher, and run the following command to install the required packages:

```
npm install
pip install -r requirements.txt
```

## Deployment

**Note:** If you wish to deploy this system, please write the `verify_account(username, code)` function within `app/custom/verify.py` yourself to implement user verification for your Online Judge. You need to make this function crawl description of `username` (or other relevant information) from the OJ and check if the description starts with the `code`. If it does, return `True`; otherwise, return `False`.

If you want to use the auto-update feature for the problems that a user has passed or attempted, please implement the function `auto_status(username)` in the file `app/custom/auto_status.py`. This function should be able to fetch the problems that the `username` has passed/attempted.

This function needs to return a dictionary, similar to:

```
{
    "1": 0,
    "5": 1,
    "7": 0
}
```

Here, the keys are the problem IDs, and the values indicate whether the problem was passed (0 means attempted, 1 means passed). If the user has not submitted a particular problem, then that key-value pair should be omitted.

Note that PID here refers to OJ ones, not this system ones.

Config file: `app/config.py`

Start the development server by running the following command in the terminal:

```
cd app
flask run
# flask run -h 0.0.0.0 -p 80
```

If you want to deploy the system, you can use gunicorn to run the Flask application:

```
pip install gunicorn
gunicorn app/app:app
```

## Development

We use Prettier and Black to format the code. Run the following command to format the code:

```
npm run format
```

We use Pylint to check the code for errors and style issues. Run the following command to check the code:

```
npm run lint
```
