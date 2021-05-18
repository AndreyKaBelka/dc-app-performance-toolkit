import random
import string

from locustio.common_utils import init_logger, jira_measure, raise_if_login_failed
from locustio.jira.requests_params import jira_datasets

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()


@jira_measure("locust_intercom_conversation_links")
def intercom_conversation_links(locust):
    raise_if_login_failed(locust)
    if jira_dataset["intercom_issues"]:
        issue_id = random.choice(jira_dataset["intercom_issues"])[1]
        r = locust.get(f'/rest/api/2/issue/{issue_id}/properties/intercom.conversation.links', catch_response=True)
        assert r.ok


def __generate_random_id(length):
    return ''.join([random.choice(string.digits) for _ in range(length)]).strip('0')


@jira_measure("locust_intercom_add_conversation")
def intercom_add_conversation(locust):
    raise_if_login_failed(locust)
    issues = jira_dataset['issues']
    issue = random.choice(issues)
    conversation_id = __generate_random_id(10)
    project_id = __get_project_id(issue[2])
    r = locust.post(f'/rest/intercom/latest/api/intercom/conversation/link?projectId={project_id}&'
                    f'conversationId={conversation_id}&issueId={issue[1]}', catch_response=True)
    assert r.ok
    if issue not in jira_dataset['intercom_issues']:
        jira_dataset['intercom_issues'].append(issue)
    jira_dataset['conversation_ids'].append((issue[1], conversation_id))


@jira_measure("locust_intercom_delete_conversation")
def intercom_delete_conversation(locust):
    raise_if_login_failed(locust)
    convs = jira_dataset['conversation_ids']
    if convs:
        conv = random.choice(convs)
        project_id = __get_project_id_for_issue_id(conv[0])
        r = locust.post(f'/rest/intercom/latest/api/intercom/conversation/link?projectId={project_id}&'
                        f'conversationId={conv[1]}&issueId={conv[0]}', catch_response=True)
        assert r.ok

        jira_dataset['conversation_ids'].remove(conv)
        issue = __get_issue_by_id(conv[0])
        if __is_conv_empty(issue[1]):
            jira_dataset['intercom_issues'].remove(issue)


def __get_project_id(key):
    for project_key, project_id in jira_dataset['projects']:
        if project_key == key:
            return project_id
    raise SystemExit(f"Project with key {key} not found")


def __get_issue_by_id(id):
    for issue in jira_dataset['issues']:
        if id == issue[1]:
            return issue
    raise SystemExit(f"Issue with id {id} not found")


def __get_project_id_for_issue_id(id):
    for key, issue_id, project_key in jira_dataset['issues']:
        if id == issue_id:
            return __get_project_id(project_key)
    raise SystemExit(f"Project not found for {id} issue")


def __is_conv_empty(id):
    for conv in jira_dataset['conversation_ids']:
        if conv[0] == id:
            return False
    return True
