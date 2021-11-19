# Keep-Me-On-Track

A WhatsApp bot built to keep track of task for the user.

The project is done using twilio, flask and sqlalchemy for the. It's deployed using heroku.

The bot responses to the following messages:

	1 .intro - About the bot && user.

	2 .pday / .pending - Work left for today.

	3 .add [task] optional[DD/MM/YY] - Adds task.

	4 .done [task] optional[DD/MM/YY]- Marks the task as done, if present.

	5 .pmonth - Work left for the month.

	6 .aday / .done - Work done today.

	7 .amonth - Work done this month.

	8 .help - Overview of the features.

