# Rating System

A concise, easy-to-configure, and powerful algorithm competition problems rating system. Developed with Python and Flask.

You can add problems to the system, rate your algorithm competition problems, or use other people's evaluations to filter problems.

## Screenshots

![](screenshots.png)

## Installation

Please install Python 3.10 or higher, Node.js 18.20 or higher, and run the following command to install the required packages:

```
npm install
pip install -r requirements.txt
```

## Deployment

**Note:** If you wish to deploy this system, please write the `verify_account(username, code)` function within `src/auth/verify.py` yourself to implement user verification for your Online Judge. You need to make this function crawl description of `username` (or other relevant information) from the OJ and check if the description starts with the `code`. If it does, return `True`; otherwise, return `False`.

Start the development server by running the following command in the terminal:

```
cd src
flask run
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
