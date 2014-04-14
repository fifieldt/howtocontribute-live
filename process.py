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


groups_json = open('etc/groups.json')
langs_json = open('etc/langs.json')

groups = json.load(groups_json)
langs = json.load(langs_json)

community_manager_email = "tom@openstack.org"

################################
# Data Methods                 #
################################


def get_group_details(group_name):
    return groups['groups'][0]


def get_lang_details(language):
    for lang in langs['langs']:
        if lang['name'] == language:
            return lang


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
    details = get_group_details(group_name)
    if group_name == "None":
        content = """=Start a User Group=
                     It looks like we couldn't find a user group in your area.

                     Are you interested in getting  a few friends together and
                     starting one?

                     Have a quick read of
                     https://wiki.openstack.org/wiki/OpenStackUserGroups/HowTo
                     and let %s know.

                     """ % community_manager_email

    else:
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

              """
    return content


def security_content():
    content = """=Join the security team=

              """
    return content


def specs_content(projects):
    content = """=Review Design Specifications=

              """

    return content


def volunteer_content():
    content = """=Volunteer with the User Committee=

              """
    return content


def main():
    email_subject = "Welcome to OpenStack"
    email_body = "Thanks for visiting our kiosk. We're looking forward to\
working with you. Here are some customised action items!\n\n\t\t"
    email_body += docs_content()
    email_body += groups_content('Australia')
    email_body += i18n_content('English (Australia)')
    email_body += infra_content()
    email_body += security_content()
    email_body += specs_content('Nova,Swift,Glance')
    email_body += volunteer_content()

    print email_body


if __name__ == "__main__":
    main()
