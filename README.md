# weekly-to-do-api

## Data Relation and Routes
### User
| field | description/type |
| ----------- | ----------- |
| username | CharField |
| password | CharField |
1. /users, POST, register user
2. /users/logout, GET, log out current user
3. /users, DELETE, delete current user
4. /users/login, POST, log in user

### Goals
| field | description/type |
| ----------- | ----------- |
| start_date | DateField |
| weekly_goal | TextField |
| user_id | ForeignKey to User |
1. /goals, POST, create week
2. /goals/start_date, GET, get weekly_goal of the week
3. /goals/start_date, PATCH, update weekly_goal of the week

### Event
| field | description/type |
| ----------- | ----------- |
| category | TextField |
| title | TextField |
| description | TextField |
| date | DateField |
| user_id | ForeignKey to User |
1. /events/id, GET, get one event data
2. /events, POST, create event
3. /events/id, DELETE, delete one event
4. /events/id, PATCH, update one event
5. /events/?start=date&days=days, GET, get all of the events from start date to limit days. (use request.args.get)

