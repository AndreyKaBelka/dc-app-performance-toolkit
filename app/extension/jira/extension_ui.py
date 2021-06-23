from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import TaskListIssue


def tasklist_create_task(webdriver, datasets):
    issue_page = TaskListIssue(webdriver, issue_id=datasets["issue_id"])

    @print_timing("selenium_create_task")
    def measure():
        @print_timing("selenium_create_task:load_issue")
        def sub_measure():
            issue_page.go_to_edit_comment()

        sub_measure()
        issue_page.create_task(datasets['rte'])

        @print_timing("selenium_create_task:submit_comment")
        def sub_measure():
            issue_page.edit_comment_submit()

        sub_measure()

    measure()


def tasklist_create_5_tasks(webdriver, datasets):
    issue_page = TaskListIssue(webdriver, issue_id=datasets["issue_id"])

    @print_timing("selenium_create_5_tasks")
    def measure():
        @print_timing("selenium_create_5_tasks:load_issue")
        def sub_measure():
            issue_page.go_to_edit_comment()

        sub_measure()
        issue_page.create_tasks(datasets['rte'], 5)

        @print_timing("selenium_create_5_tasks:submit_comment")
        def sub_measure():
            issue_page.edit_comment_submit()

        sub_measure()

    measure()


def tasklist_create_issue_with_tasks(webdriver, datasets):
    issue_page = TaskListIssue(webdriver, issue_key=datasets["issue_key"])

    @print_timing("selenium_create_issue_with_tasks")
    def measure():
        @print_timing("selenium_create_issue_with_tasks:open_quick_create")
        def sub_measure():
            issue_page.open_create_issue_modal()

        sub_measure()

        @print_timing("selenium_create_issue_with_tasks:submit_comment")
        def sub_measure():
            issue_page.fill_summary_create()  # Fill summary field
            issue_page.fill_description_create(datasets['rte'])  # Fill description field
            issue_page.assign_to_me()  # Click assign to me
            issue_page.set_resolution()  # Set resolution if there is such field
            issue_page.set_issue_type()  # Set issue type, use non epic type

            @print_timing("selenium_create_issue_with_tasks:submit_comment:submit_issue_form")
            def sub_sub_measure():
                issue_page.submit_issue()

            sub_sub_measure()

        sub_measure()

    measure()


def tasklist_edit_issue_with_tasks(webdriver, datasets):
    issue_page = TaskListIssue(webdriver, issue_id=datasets['custom_issue_id'])

    @print_timing("selenium_edit_issue_with_tasks")
    def measure():
        @print_timing("selenium_edit_issue_with_tasks:load_issue")
        def sub_measure():
            issue_page.go_to_edit_issue()

        sub_measure()

        issue_page.fill_summary_edit()
        issue_page.edit_issue_with_tasks(datasets['rte'])

        @print_timing("selenium_edit_issue_with_tasks:submit_issue")
        def sub_measure():
            issue_page.edit_issue_submit()
            issue_page.wait_for_issue_title()

        sub_measure()

    measure()
