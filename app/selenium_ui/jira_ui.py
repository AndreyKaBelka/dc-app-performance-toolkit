from extension.jira import extension_ui  # noqa F401
from selenium_ui.jira import modules


# this action should be the first one
def test_0_selenium_a_login(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.login(jira_webdriver, jira_datasets)


def test_1_selenium_like_jql(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.tasklist_like_jql(jira_webdriver, jira_datasets)


def test_1_selenium_is_jql(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.tasklist_is_jql(jira_webdriver, jira_datasets)


def test_1_selenium_eq_jql(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.tasklist_eq_jql(jira_webdriver, jira_datasets)


def test_1_selenium_tasklist_create_task(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.tasklist_create_task(jira_webdriver, jira_datasets)


def test_1_selenium_tasklist_create_5_tasks(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.tasklist_create_5_tasks(jira_webdriver, jira_datasets)


def test_1_selenium_tasklist_create_issue_with_tasks(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.tasklist_create_issue_with_tasks(jira_webdriver, jira_datasets)


def test_1_selenium_tasklist_edit_issue_with_tasks(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui.tasklist_edit_issue_with_tasks(jira_webdriver, jira_datasets)


# this action should be the last one
def test_2_selenium_z_log_out(jira_webdriver, jira_datasets, jira_screen_shots):
    modules.log_out(jira_webdriver, jira_datasets)
