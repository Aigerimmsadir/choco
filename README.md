# chocotodo project
## SETUP:
USE VS Code
open root folder, CTRL-Shift-P "Rebuild and Reopen in container"

then in terminal type:
python3 manage.py runserver
or in "Run and Debug" bar tap button "Run server"

environment variables file is located in .devcontainer/.credentials/.devcontainer.env
fill email and email_password fields


## API:

**registration**:
 */api/user/*  [POST]
   required fields:
      username, email, password

**login** - */api/login* [POST]
  required fields:: 
    username, password

**list of tasks**: *api/task/* [GET]

**new task**: *api/task/* [POST]

**update task with ID**: i *api/task/{pk}/* [PUT]

**delete task with ID**: i *api/task/pk/* [DELETE]

**get task by status**: *api/task/tasks_by_status/* [GET]
    required fields:
        status (integer 0,1 or 2)
        
**send statistics**: *api/send_statistics/* [POST]
