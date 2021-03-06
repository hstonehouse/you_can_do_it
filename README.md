# Heroku Link
[You Can Do It App](https://youcandoit-app.herokuapp.com/)

# YOU CAN DO IT!
We are more likely to achieve our goals when we have an accountability buddy.

This app is designed to share your goals with your friends so that they can act as an accountability buddy and help you achieve those goals!

Create an account, list your goals, add your friends, and see each other's goals. Click on the 'nudge' button next to your friend's goal to remind them to work on that goal.

# Tech Stack
- HTML/CSS
- Python/Flask
- postgreSQL

# Installation (Python)
Create a virtual environment:

    python -m venv nameofvenv

Activate the virtual environment:

    source venv/bin/activate

I have included all the modules used in a file called "requirements.txt".
Please install it by running the following code:

    pip install -r requirements.txt    

To run the app, paste this in your terminal:

    python app.py

Note: the Procfile is only needed if you are deploying to Heroku.

# Installation (Database)
1. Open the setup.sql file
2. Copy and paste the 2 steps in your terminal

# Future Improvements
Things I'd like to add:
- Ability to prioritise your goals
- A drop down menu to sort your goals by different parameters (ascending, descending, priority)
- Option to delete a friend
- Option to undo your nudge
- JavaScript to incorporate notifications when someone nudges a goal
- Fix the code so that you cannot add the same friend more than once
- Option to 'tick off' your goal, and have that move to a section called 'Accomplished Goals'
- Have some sort of animation appear when you tick off a goal
