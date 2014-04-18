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

import json
import ast

groups_json = open('etc/groups.json')
langs_json = open('etc/langs.json')
projects_json = open('etc/projects.json')

groups = json.load(groups_json)
langs = json.load(langs_json)
projects = json.load(projects_json)

community_manager_email = "tom@openstack.org"

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
    content = """=Find out about Docs=

              Thanks for asking about OpenStack documentation.

              We have a range of documentation to read, and welcome
              contributors from people like yourself who are using the
              software.

              A good place to get started is ...

              We also have ....

              If you find any problems with the docs, just click the red
              bug in the corner and type something up about what's wrong.

              It's actually pretty easy to patch things up and ....

              """

    return content


def groups_content(group_name):
    if group_name == "NotFound":
        content = """=Start a User Group=
                     It looks like we couldn't find a user group in your area.

                     Are you interested in getting  a few friends together and
                     starting one?

                     Have a quick read of
                     https://wiki.openstack.org/wiki/OpenStackUserGroups/HowTo
                     and let %s know.

                     """ % community_manager_email

    else:
        details = get_group_details(group_name)
        content = """=Join your User Group=

                     You can join %s at this URL:

                     If you run into any issues, you can contact

                     %s
                     %s

                     """ % (group_name, details["coordinators"],
                            details["coordinator_emails"])

    return content


def i18n_content(language):
    details = get_lang_details(language)
    content = """=Translate OpenStack=

                 Thanks for your interest in translating into %s.

                 Beginning to translate is simple - instructions at:
                 https://wiki.openstack.org/wiki/Documentation/Translation#Contribute_as_a_translator

                 Your language coordinator is %s.

                 You may also want to join the OpenStack-i18N mailing list at
                 http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-i18n


                 """ % (language, details["coordinator_email"])

    return content


def infra_content():
    content = """=Join the infrastructure team=
               Keeping a thousand developers working is hard. The OpenStack
               infrastructure team welcomes your help at:
               http://ci.openstack.org/project.html#contributing
              """
    return content


def security_content():
    content = """=Join the security team=
                There's never enough good security people around. You can find
                ways to help out the OpenStack Security Group (OSS) here:
                 https://wiki.openstack.org/wiki/Security/How_To_Contribute
              """
    return content


def specs_content(projects):
    content = """=Review Design Specifications=
                 OpenStack follows the principle of Open Design, meaning that
                 all features are discussed on public websites, and you can
                 review and contribute to them.

                 One area we need help is for people running clouds to have a
                 look at the planned features and make suggestions.

                 To host the work, some projects use a code review system
                 (Gerrit), and others use the Launchpad blueprints system. The
                 URLs for the projects you are interested in are below:

              """
    for project in projects:
        content += project + ": " + get_project_details(project)["url"] + "\n"

    return content


def volunteer_content():
    content = """=Volunteer with the User Committee=
                The User Committe needs help in a range of areas. Please check
                out this form:
https://docs.google.com/a/openstack.org/forms/d/1HOwsPp44fNbWv9zgvXW8ZnCaKszg_XKu7vmLbrPFMzQ/viewform
              """
    return content


################################
# Action Methods               #
################################

def subscribe_mls(email, mls):
    for ml in mls:
        print "sending an email with subject=subscribe to " + ml + "-request@lists.openstack.org"

def process_response(response):
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
        subscribe_mls(response_dict["Email"], mls)
    if len(specs) > 0:
        email_body += specs_content(specs)

    print email_body


def main():
    responses = get_responses()
    for response in responses:
        process_response(response)


if __name__ == "__main__":
    main()
