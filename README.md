# jira-ticket
This script interacts with the Jira API and the File Explorer. 

Queries Jira to find all issues that fit pre-defined JQL, then links them to a newly created Jira issue. 
Basic data metrics, such as number of tickets are returned so that user can ensure all data is being collected by script.
Script then navigates the file explorer, based on date specific naming conventions, and attaches a file that meets the naming criteria.
All issues initially returned by JQL are then transitioned into an `intermediate` status and then into a `closed` status.

Important to note that that while I currently use this tool, it is designed to eventually be used by non-technical stakeholders. So it is designed very incrementally and with several user "quality check" steps, to ensure that all inputs are accurate.

Time Savings: Process orginally took ~1hr to complete and now takes ~5min. Over the course of the week ~4.5hrs saved
