# weekly-to-do-api

## Data Relation and Routes
### User
| field | description/type |
| ----------- | ----------- |
| username | CharField |
| password | CharField |
1. /user, POST, register user
2. /user, GET, log out current user
3. /user, DELETE, delete current user
4. /user/login, POST, log in user

### Week
| field | description/type |
| ----------- | ----------- |
| start_date | DateField |
| weekly_goal | TextField |
| user_id | ForeignKey to User |
1. /week, POST, create week
2. /week, GET, get week data
3. /week, PATCH, update weekly_goal

### Day
| field | description/type |
| ----------- | ----------- |
| date | DateField |
| note | TextField |
| week_id | ForeignKey to Week |
1. /day, POST, create day
2. /day, GET, get day data
3. /day, PATCH, update note

### Event
| field | description/type |
| ----------- | ----------- |
| type | TextField |
| title | TextField |
| description | TextField |
| day_id | ForeignKey to Day |
1. /event, GET, get event data
2. /event, POST, create event
3. /event, DELETE, delete event
4. /event, PATCH, update event
 
