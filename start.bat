REM The GUI for GAE, on Windows, has a but, therefore we need to pass some parameters "by hand"
REM Use a tool like Papercut to test the app sending emails.
REM Application will be reachable at localhost:8080
REM Admin interface at localhost:8001
python "c:\Program Files (x86)\Google\google_appengine\dev_appserver.py" --port=8080 --admin_port=8001 pyGAE --smtp_host=localhost --smtp_port=25