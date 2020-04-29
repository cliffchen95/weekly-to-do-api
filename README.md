# to-do-api

## data relation
### User
| field | description/type |
| ----------- | ----------- |
| username | CharField |
| password | CharField |
### Week
| field | description/type |
| ----------- | ----------- |
| start_date | DateField |
| weekly_goal | TextField |
| user_id | ForeignKey to User |
### Day
| field | description/type |
| ----------- | ----------- |
| date | DateField |
| note | TextField |
| week_id | ForeignKey to Week |
### Event
| field | description/type |
| ----------- | ----------- |
| type | TextField |
| title | TextField |
| description | TextField |
| day_id | ForeignKey to Day |
 