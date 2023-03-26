# LogWatchdog
This script is analysis the server log and restart services when found specific expression and send information email.

The script scans the server log for the specified expression. If the expression is found, it resets the services using an external script and waits for a new log until the next day. Otherwise, it waits for an hour and scans again. Running status is written to the status.log file.
