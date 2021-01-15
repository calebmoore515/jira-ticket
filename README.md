# jira-ticket

#### Description

This script interacts with the Jira API and the File Explorer. 

Queries Jira to find all issues that fit pre-defined JQL, then links them to a newly created Jira issue. 
Basic data metrics, such as number of tickets are returned so that user can ensure all data is being collected by script.
Script then navigates the file explorer, based on date specific naming conventions, and attaches a file that meets the naming criteria.
All issues initially returned by JQL are then transitioned into an `intermediate` status and then into a `closed` status.

Important to note that that while I currently use this tool, it is designed to eventually be used by non-technical stakeholders. So it is designed very incrementally and with several user "quality check" steps, to ensure that all inputs are accurate.

#### Time Saved

Process orginally took ~1hr to complete and now takes ~5min. Over the course of the week ~4.5hrs saved

#### Troubleshooting

1. Be sure you are logged onto proper VPN

2. Jira credintials are up to date (changes every 90 days)

3. If the script fails to attach the document from ZFS, be sure that you are logged into File Explorer (LDAP Creds) and that the file follows the proper naming convention `DLX Customs Update yyyyddmm.csv`. The file will need to be manually attached.

      3A. Also check the naming convention of the folder storing the final file. It should           be named `yyyydd` where the day represents the Monday of that week. This can               cause problems on weeks where Monday was a holiday, the folder is accidentally             mis-named. Update naming and then manually attach the file.
      
#### Future improvements 

It would be good to upgrade the error handling for issues with the naming convention ( \#3/3A in troubleshooting list). As it exists now, if this step fails the file needs to be manually attached and then the linked tickets need to be manually closed. Upgrade where this step can be re-run once the naming is corrected, or print the error and them move on to the next step in the code.
