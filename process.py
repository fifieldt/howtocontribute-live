#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Processing backend.

Takes actions based on what the form captured.
"""

import argparse
import ast
import json
import logging
import smtplib

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
sender_email = "tom@openstack.org"
sender_password = ""

logger = logging.getLogger('howtocontribute-live')

groups_json = open('etc/groups.json')
langs_json = open('etc/langs.json')
projects_json = open('etc/projects.json')

groups = json.load(groups_json)
langs = json.load(langs_json)
projects = json.load(projects_json)


################################
# Data Methods                 #
################################


def get_group_details(group_name):
    for group in groups['groups']:
        if group['group'] == group_name:
            return group


def get_lang_details(language):
    for lang in langs['langs']:
        if lang['name'] == language:
            return lang


def get_project_details(project_name):
    for project in projects['projects']:
        if project['name'] == project_name:
            return project


def get_responses():
    responses = open('responses.txt')
    return responses

################################
# Content Methods              #
################################


def docs_content():
    content = """
*Find out about Docs*

Thanks for asking about OpenStack documentation.

We have a range of documentation to read, and welcome contributors from people
 like yourself who are using the software.

A good place to get started is the install guides at:
http://docs.openstack.org/.

We also have the Operations Guide and Security Guide at:
http://docs.openstack.org/ops
http://docs.openstack.orgs/sec

If you find any problems with the docs, just click the red bug in the corner and
type something up about what's wrong.

It's actually pretty easy to patch things up. Check out this guide:
https://wiki.openstack.org/wiki/Documentation/HowTo/FirstTimers

I you have any issues, join the #OpenStack-doc IRC channel
https://wiki.openstack.org/wiki/IRC\n\n"""

    return content


def groups_content(group_name):
    if group_name == "NotFound":
        content = """
*Start a User Group*
It looks like we couldn't find a user group in your area.

Are you interested in getting a few friends together and starting one?

Have a quick read of
https://wiki.openstack.org/wiki/OpenStackUserGroups/HowTo
and let %s know.
                     """ % sender_email

    else:
        details = get_group_details(group_name)
        if details["meetup_url"] != "":
            url = details["meetup_url"]
        elif details["ml_url"] != "":
            url = details["ml_url"]
        elif details["facebook_url"] != "":
            url = details["facebook_url"]
        elif details["gplus_url"] != "":
            url = details["gplus_url"]
        elif details["linkedin_url"] != "":
            url = details["linkedin_url"]
        elif details["website_url"] != "":
            url = details["website_url"]
        elif details["microblog_url"] != "":
            url = details["microblog_url"]

        content = """
*Join your User Group*

You can join the %s group at this URL:

%s

If you run into any issues, you can contact

%s
%s

                     """ % (group_name, url, details["coordinators"],
                            details["coordinator_emails"])

    return content


def i18n_content(language):
    if language == "NotFound":
        content = """
*Translate OpenStack*
It looks like we don't have your language in the list yet.

Are you interested in getting people together and starting a translation team?

Have a look https://wiki.openstack.org/wiki/I18nTeam/CreateLocalTeam
and let guoyingc@cn.ibm.com know!
                  """
    else:
        details = get_lang_details(language)
        if "coordinator_email" not in details.keys():
            details["coordinator_email"] = """Unknown. Please contact Daisy at
                                            guoyingc@cn.ibm.com for more
                                            assistance."""
        content = """
*Translate OpenStack*

Thanks for your interest in translating into %s.

Beginning to translate is simple - instructions at:
https://wiki.openstack.org/wiki/Documentation/Translation#Contribute_as_a_translator

Your language coordinator is %s.

You may also want to join the OpenStack-i18N mailing list at
http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-i18n

                     """ % (language, details["coordinator_email"])

    return content


def infra_content():
    content = """
*Join the infrastructure team*
Keeping a thousand developers working is hard.
The OpenStack infrastructure team welcomes your help at:
http://ci.openstack.org/project.html#contributing\n\n
"""
    return content


def security_content():
    content = """
*Join the security team*
You can never have too many good security people around.
You can find ways to help out the OpenStack Security Group (OSS) here:
https://wiki.openstack.org/wiki/Security/How_To_Contribute\n\n
              """
    return content


def specs_content(projects):
    content = """
*Review Design Specifications*
OpenStack follows the principle of Open Design, meaning that all features are
discussed on public websites, and you can review and contribute to them.

One area we need help is for people running clouds to have a look at the
planned features and make suggestions.

To host the work, some projects use a code review system (Gerrit), and others
use the Launchpad blueprints system. The URLs for the projects you are
interested in are below:

"""
    for project in projects:
        content += project + ": " + get_project_details(project)["url"] + "\n"

    return content


def volunteer_content():
    content = """
*Volunteer with the User Committee*
The User Committe needs help in a range of areas. Please check out this form:
https://docs.google.com/a/openstack.org/forms/d/1HOwsPp44fNbWv9zgvXW8ZnCaKszg_XKu7vmLbrPFMzQ/viewform\n\n
              """
    return content


################################
# Action Methods               #
################################

def subscribe_mls(email, mls, dryrun):
    for ml in mls:
        logger.debug("sending an email with subject=subscribe to " + ml + "-request@lists.openstack.org")
        if ml not in ["announce", "docs", "i18n", "infra", "operators" "security"]:
            logger.error("Tried to sign up to a non-existent list. Failing.")
            break
        if not dryun:
            headers = ["from: " + email,
                       "subject: subscribe",
                       "to: " + ml + "-request@lists.openstack.org",
                       "mime-version: 1.0",
                       "content-type: text/plain"]
            headers = "\r\n".join(headers)
            s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            if SMTP_PORT == 587:
                s.starttls()
                s.login(sender_email, sender_password)
            s.sendmail(email, ml + "-request@lists.openstack.org", headers)


def process_response(response, dryrun):
    response_dict = ast.literal_eval(response)
    email_subject = "Welcome to OpenStack"
    email_body = "Thanks for visiting our kiosk. We're looking forward to\
 working with you. Here are some customised action items!\n\n\t\t"

    mls = []
    specs = []

    for key, value in response_dict.iteritems():
        if "MLs" in key:
            mls.append(value)
        if "ProjectsUsed" in key:
            specs.append(value)
        if key == "Interests[docs]":
            email_body += docs_content()
        if key == "UserGroup" and value != "None":
            email_body += groups_content(value)
        if key == "Language" and value != "None":
            email_body += i18n_content(value)
        if key == "Interests[infra]":
            email_body += infra_content()
        if key == "Interests[security]":
            email_body += security_content()
        if key == "Interests[committee]":
            email_body += volunteer_content()

    if len(mls) > 0:
        subscribe_mls(response_dict["Email"], mls, dryrun)
    if len(specs) > 0:
        email_body += specs_content(specs)

    logger.debug(email_body)
    logger.debug(response_dict["Email"])

    if not dryrun:
        s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        if SMTP_PORT == 587:
            s.starttls()
            s.login(sender_email, sender_password)
        headers = ["from: " + sender_email,
                   "subject: " + email_subject,
                   "to: " + response_dict["Email"],
                   "mime-version: 1.0",
                   "content-type: text/plain"]
        headers = "\r\n".join(headers)
        s.sendmail(sender_email, response_dict["Email"], headers + "\r\n\r\n" + email_body)
        s.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dryrun', dest='dryrun', action='store_true')
    parser.add_argument('--no-dryrun', dest='dryrun', action='store_false')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='verbose output')
    parser.set_defaults(dryrun=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    responses = get_responses()
    for response in responses:
        process_response(response, args.dryrun)


if __name__ == "__main__":
    main()
