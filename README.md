# jira-ticket
This script interacts with the Jira API and the File Explorer. 

Queries Jira to find all issues that fit pre-defined JQL, then links them to a newly created Jira issue. 
Basic data metrics, such as number of tickets are returned so that user can ensure all data is being collected by script.
Script then navigates the file explorer, based on date specific naming conventions, and attaches a file that meets the naming criteria.
All issues initially returned by JQL are then transitioned into an `intermediate` status and then into a `closed` status.
