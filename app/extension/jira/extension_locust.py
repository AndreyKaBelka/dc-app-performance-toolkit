import random
import re
import string

from locustio.common_utils import init_logger, jira_measure, RESOURCE_HEADERS, fetch_by_re, ADMIN_HEADERS, \
    raise_if_login_failed
from locustio.jira.requests_params import jira_datasets, CreateIssue

logger = init_logger(app_type='jira')
jira_dataset = jira_datasets()


@jira_measure("locust_create_task")
def create_task(locust):
    issue_key = random.choice(jira_dataset['issues'])[0]
    r = locust.post('/rest/tasklist/1.0/tasks',
                    json=__get_task_json(issue_key),
                    headers=RESOURCE_HEADERS,
                    catch_response=True)
    content = r.content.decode('utf-8')
    assert "id" in content


@jira_measure("locust_create_5_tasks")
def create_5_tasks(locust):
    issue_key = random.choice(jira_dataset['issues'])[0]
    r = locust.post(f'/rest/tasklist/1.0/tasks/bulk?issueKey={issue_key}',
                    json=[__get_task_json(issue_key) for _ in range(5)],
                    headers=RESOURCE_HEADERS,
                    catch_response=True)
    content = r.content.decode('utf-8')
    assert "id" in content


def create_issue_with_tasks(locust):
    params = CreateIssue()
    project = random.choice(jira_dataset['projects'])
    project_id = project[1]

    @jira_measure('locust_create_issue_with_tasks:open_quick_create')
    def create_issue_open_quick_create():
        raise_if_login_failed(locust)

        # 200 /secure/QuickCreateIssue!default.jspa?decorator=none
        r = locust.post('/secure/QuickCreateIssue!default.jspa?decorator=none', ADMIN_HEADERS, catch_response=True)

        content = r.content.decode('utf-8')
        atl_token = fetch_by_re(params.atl_token_pattern, content)
        form_token = fetch_by_re(params.form_token_pattern, content)
        issue_type = fetch_by_re(params.issue_type_pattern, content)
        resolution_done = fetch_by_re(params.resolution_done_pattern, content)
        fields_to_retain = re.findall(params.fields_to_retain_pattern, content)
        custom_fields_to_retain = re.findall(params.custom_fields_to_retain_pattern, content)

        issue_body_params_dict = {'atl_token': atl_token,
                                  'form_token': form_token,
                                  'issue_type': issue_type,
                                  'project_id': project_id,
                                  'resolution_done': resolution_done,
                                  'fields_to_retain': fields_to_retain,
                                  'custom_fields_to_retain': custom_fields_to_retain
                                  }

        if not ('"id":"project","label":"Project"' in content):
            logger.error(f'{params.err_message_create_issue}: {content}')
        assert '"id":"project","label":"Project"' in content, params.err_message_create_issue

        # 205 /rest/quickedit/1.0/userpreferences/create
        locust.post('/rest/quickedit/1.0/userpreferences/create',
                    json=params.user_preferences_payload,
                    headers=ADMIN_HEADERS,
                    catch_response=True)

        # 210 /rest/analytics/1.0/publish/bulk
        locust.post('/rest/analytics/1.0/publish/bulk',
                    json=params.resources_body.get("210"),
                    headers=RESOURCE_HEADERS,
                    catch_response=True)

        locust.session_data_storage['issue_body_params_dict'] = issue_body_params_dict

    create_issue_open_quick_create()

    @jira_measure('locust_create_issue_with_tasks:fill_and_submit_issue_form')
    def create_issue_submit_form():
        raise_if_login_failed(locust)
        issue_body = params.prepare_issue_body(locust.session_data_storage['issue_body_params_dict'],
                                               user=locust.session_data_storage["username"],
                                               description=__create_task_macro(20))

        # 215 /secure/QuickCreateIssue.jspa?decorator=none
        r = locust.post('/secure/QuickCreateIssue.jspa?decorator=none',
                        params=issue_body,
                        headers=ADMIN_HEADERS,
                        catch_response=True)

        # 220 /rest/analytics/1.0/publish/bulk
        locust.post('/rest/analytics/1.0/publish/bulk',
                    json=params.resources_body.get("220"),
                    headers=RESOURCE_HEADERS,
                    catch_response=True)

        content = r.content.decode('utf-8')
        if '"id":"project","label":"Project"' not in content:
            logger.error(f'{params.err_message_create_issue}: {content}')
        assert '"id":"project","label":"Project"' in content, params.err_message_create_issue
        issue_key = fetch_by_re(params.create_issue_key_pattern, content)
        logger.locust_info(f"{params.action_name}: Issue {issue_key} was successfully created")

    create_issue_submit_form()


def __create_task_macro(task_count=5) -> str:
    return "".join([f'{{task}}{__random_string()}{{task}}' for _ in range(task_count)])


def __random_string(length: int = 15) -> str:
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


def __get_task_json(issue_key: str) -> dict:
    return {"text": __random_string(20), "issue": issue_key}
