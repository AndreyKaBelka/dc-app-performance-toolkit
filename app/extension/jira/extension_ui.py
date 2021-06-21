import random

from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import TaskListIssue, PopupManager


def tasklist_create_tasks(webdriver, datasets):
    issue_page = TaskListIssue(webdriver, issue_key=datasets["issue_key"])

    @print_timing("selenium_create_tasks")
    def measure():
        @print_timing("selenium_create_tasks:edit_issue")
        def sub_measure():
            issue_page.go_to()
            issue_page.wait_for_page_loaded()

        sub_measure()

        @print_timing("selenium_create_tasks:create_tasks")
        def sub_measure():
            issue_page.create_tasks(count=random.randrange(5, 10))

        sub_measure()

    measure()
    PopupManager(webdriver).dismiss_default_popup()


def tasklist_delete_tasks(webdriver, datasets):
    issue_page = TaskListIssue(webdriver, issue_key=datasets["custom_issue_key"])

    @print_timing("selenium_delete_tasks")
    def measure():
        @print_timing("selenium_delete_tasks:load_page")
        def sub_measure():
            issue_page.go_to()
            issue_page.wait_for_page_loaded()

        sub_measure()

        @print_timing("selenium_delete_tasks:delete_tasks")
        def sub_measure():
            issue_page.delete_task()

        sub_measure()

    measure()
    PopupManager(webdriver).dismiss_default_popup()


def tasklist_edit_tasks(webdriver, datasets):
    issue_page = TaskListIssue(webdriver, issue_key=datasets["custom_issue_key"])

    @print_timing("selenium_delete_tasks")
    def measure():
        @print_timing("selenium_delete_tasks:load_page")
        def sub_measure():
            issue_page.go_to()
            issue_page.wait_for_page_loaded()

        sub_measure()

        @print_timing("selenium_delete_tasks:delete_tasks")
        def sub_measure():
            issue_page.edit_task()

        sub_measure()

    measure()
    PopupManager(webdriver).dismiss_default_popup()
