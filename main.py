# 	                   [\
#             .----' `-----.                Welcome to Taxi, here's some general notes...
#            //^^^^;;^^^^^^`\
#    _______//_____||_____()_\________      Written by Caleb Moore (bug him with any questions)
#  /585     :      : ___              `\    Initially written May 2019
#  |>   ____;      ;  |/\><|   ____   _<)   Updated for 585 in July 2019
# {____/    \_________________/    \____}   Creates taxonomy ticket, links the strategies, attaches taxonomy doc from
#      \ '' /                 \ '' /        ZFS, and then closes the fulfillment tickets.
#       '--'                   '--'

# Be sure all fulfillment tickets are marked with a cf label
# Be sure to update the mapping before running this script. The mapping automation relies on the fulfillment tickets
# being open when it runs. If you accidentally run before, you'll just need to update the mapping manually.

# When naming your taxonomy documents, be sure to name the folder using the date of the Monday of that week and be sure
# that the file itself follows the specific naming convention, or the script will not pick it up and will error out

from jira.client import JIRA  # --> installed with `pip install jira` in the terminal
import datetime
import sys

count = 0
count1 = 0
check_count = 0
lab_count = 0

# <editor-fold desc="Jira Creds">
options = {'server': 'server_address.com'}
jira = JIRA(options, basic_auth=('username', 'pass'))
# </editor-fold>

#JQL used to identify target tickets 

issues_in_proj = jira.search_issues('project = ABC AND issuetype in ("Ticket Type") '
                                    'AND status = Open AND cf[12345] ~ Platform AND "Fulfill Channel ID" ~ 123 '
                                    'AND labels = "cf"', maxResults=50)

print('Initiating Taxi Automation\n')

no_sync = []
issues_in_proj_sync = []
listed = []

#This loop filters tickets based on a boolean field in Jira. Determines if data needs to be synced to additional component.

for issue in issues_in_proj:
    if "Branded" in issue.raw['fields']['summary']:
        no_sync.append(issue)
    elif issue.fields.customfield_45678 == 'true':
        check_count += 1
    elif issue.fields.customfield_45678 == 'false':
        check_count += 1

#QC step for the user, allows them to verify everything is functioning as expected. Basic error handling built in        

check_input = str(input('There are currently ' + str(check_count) + ' tickets in the queue, does this match the '
                                                                    'number counted in BK Taxo Script? (Y/N): '))

if check_input.lower() == 'y':
    print('\nSweet, proceeding with automation\n')
elif check_input.lower() == 'n':
    print('\nA new ticket has likely been submitted since you started, omit it with proper JQL (AND issue != '
          'CAM-12345) - Exiting program\n')
    sys.exit(0)
else:
    print('\nInvalid input, re-run program\n')
    sys.exit(0)

#User input required to help populate the description field in the newly created ticket    

whitelist_req = str(input('Is Whitelisting Required (Y/N): '))
pid = str(input('What is the PID (comma delimited if multiple - N/A if null): '))

print('\nLast chance to exit before writing to Jira')
create_y_n = str(input('Is the info above correct? (Y/N): '))

if create_y_n.lower() == 'y':
    print('\nCreating the ticket now\n')
elif create_y_n.lower() == 'n':
    print('\nExiting program, no ticket has been created\n')
    sys.exit(0)

#Creating ticket - Date, PID, and whitelist req are all dynamic fields     

title = 'New DLX Custom Categories ' + str(datetime.date.today())

desc = 'New segments attached. Please create and confirm.\n' \
       '\nThanks!' \
       '\nCaleb\n' \
       '\nWhitelisting Required (Y/N): ' + str(whitelist_req.upper()) + \
       '\nIf Y, Whitelist PID: ' + str(pid.upper()) + \
       '\n2. Existing Rules (Replace/Append/Delete/Change/NA): N/A' \
       '\n3. Site Switch ID Required (Y/N): N' \
       '\nIf Y, Site Switch ID: N/A'


issue_dict = {
    'project': 'TAXO',
    'summary': title,
    'description': desc,
    'issuetype': {'name': 'Branded/PDM'},
    'customfield_34567': [{"value": "Custom"}, {"value": "DLX"}],
    'customfield_45678': 'All',
    'customfield_56789': '1',
    'customfield_67890': {"value": "Fulfillment"},
    'customfield_78901': ['Datalogix']
}
new_issue = jira.create_issue(fields=issue_dict)

print('Congrats, you have created ' + str(new_issue))

print('Assigning it to Campaign Fulfillment')

#Routes ticket to proper team 

jira.assign_issue(new_issue, 'campaignfulfillment')

print('Ticket successfully assigned\n')

print('If there was whitelisting involved then you need to manually provide sample paths in ticket!\n')

link_y_n = str(input('You have created a taxonomy ticket! Do you want to continue and link issues? (Y/N): '))

if link_y_n.lower() == 'y':
    print('\nLinking tickets now\n')
elif link_y_n.lower() == 'n':
    print('\nExiting program, you will need to manually link tickets and attach the taxonomy doc\n')
    sys.exit(0)
else:
    print('\nInvalid input, manually complete or run modular scripts\n')
    sys.exit(0)


taxo_issue = jira.issue(new_issue)

print('Linked the following issues to: https://jira.server.com/browse/' + str(new_issue) + '\n')

#Links all sub issues to the newly created parent issue

for issue in issues_in_proj:
        strategy = jira.search_issues('issue in linkedIssues(' + str(issue) + ', "Strategy") AND status in (Audience, '
                                                                              '"Scorecard Approval", "Post Processing")')
        issues_in_proj_sync.append(str(issue))
        for issue in strategy:
            strategy_issue = jira.issue(issue)
            jira.create_issue_link('relates to', taxo_issue, strategy_issue)
        print('https://jira.server.com/browse/' + str(issue))
        count += 1

print('\n' + str(count) + ' strategies linked!\n')

attach_y_n = str(input('You linked the strategies! Do you want to continue and attach the taxo doc? (Y/N): '))

if attach_y_n.lower() == 'y':
    print('\nAttaching doc from ZFS now\n')
elif attach_y_n.lower() == 'n':
    print('\nExiting program, you will need to manually attach the taxonomy document\n')
    sys.exit(0)
else:
    print('\nInvalid input, manually complete or run modular scripts\n')
    sys.exit(0)

today_1 = datetime.date.today()
d = ((today_1) - datetime.timedelta(days=today_1.weekday()))
monday_date = d.strftime("%Y%m%d")
today = (time.strftime('%Y%m%d'))

#QC Step for user, ensures file naming convention is correct

print("Is this today's date: " + today)
print("Was this Monday's date: " + monday_date)
print('Check against file naming conventions')
user_input = str(input('Y/N: '))

if user_input.lower() == 'y':
    print('\nPhew, everything is working properly\n')
elif user_input.lower() == 'n':
    print('\nError with dates, manually attach taxonomy document\n')
    sys.exit(0)
else:
    print('\nInvalid input, manually complete or run modular scripts\n')
    sys.exit(0)

# Must be logged into ZFS in file explorer, file path is dynamic based on date
path = '//zfs1/Operations/Audience_Ops/DLX Customs/' + str(formatted_date) + '/DLX Customs Update ' + str(today) + '.csv'

jira.add_attachment(issue=new_issue, attachment=path)

close_y_n = str(input('You attached to taxonomy document! Would you like to close the fulfillment tickets? (Y/N): '))

if close_y_n.lower() == 'y':
    print('\nClosing fulfillment tickets now\n')
elif close_y_n.lower() == 'n':
    print('\nExiting program, you will need to manually close all related fulfillment tickets\n')
    sys.exit(0)
else:
    print('\nInvalid input, manually complete or run modular scripts\n')
    sys.exit(0)

#Hits Jira API to transition all sub tickets to intermediate stage and the closed stage
    
for issue in issues_in_proj:
        print('https://jira.server.com/browse/' + str(issue))
        jira.transition_issue(issue, transition='55')
        print('Transitioned to Waiting for Metadata')
        jira.transition_issue(issue, transition='65')
        print('Transitioned to Complete')
        count1 += 1

print('\n' + str(count1) + ' fulfillment tickets closed!')

#Removes label used to query tickets. Purely cosmetic, but helps keep unnecessary info from staying on tickets

issues_in_proj_1 = jira.search_issues('project = ABC AND issuetype in ("Ticket Type") '
                                      'AND status = Complete AND cf[12345] ~ Platform AND "Fulfill Channel ID" ~ 123 '
                                      'AND labels = "cf"', maxResults=20)

print('\nRemoving labels - This can take up to a minute')

# This API call is used to remove the label from the ticket. We have moved away from labels, so we don't want to leave
# them on tickets. They should only be present during taxonomy creation

for issue in issues_in_proj_1:
    issue.update(fields={"labels": [' ']})
    lab_count += 1

print('Removed ' + str(lab_count) + ' labels')

#Final user instructions

print('\nYou have completed DLX Custom taxonomy')
print('Remember, if there was whitelisting involved then you need to manually provide sample paths in ticket!')

print('\nPID: Datalogix Private > New Node Name')
