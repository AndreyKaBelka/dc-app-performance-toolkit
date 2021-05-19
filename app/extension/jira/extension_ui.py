from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Issue, IntercomIssue
from selenium_ui.jira.pages.selectors import IntercomSelectors


def intercom_issue_load_action(webdriver, datasets):
    intercom_issue_page = IntercomIssue(webdriver, issue_key=datasets['intercom_issue'][0])
    print(datasets)

    @print_timing('selenium_intercom_issue_load')
    def measure():
        intercom_issue_page.go_to()
        intercom_issue_page.wait_for_page_loaded()

    measure()


def intercom_add_link_to_issue_action(webdriver, datasets):
    intercom_issue_page = IntercomIssue(webdriver, issue_key=datasets['intercom_issue'][0])

    @print_timing('selenium_intercom_add_link')
    def measure():
        @print_timing('selenium_intercom_add_link:load_issue')
        def sub_measure():
            intercom_issue_page.go_to()
            intercom_issue_page.wait_for_page_loaded()

        sub_measure()

        @print_timing('selenium_intercom_add_link:click_add_link_button')
        def sub_measure():
            con_url = intercom_issue_page.generate_link_url(intercom_issue_page.generate_random_id(10))

            intercom_issue_page.wait_until_clickable(IntercomSelectors.add_link_button).click()
            intercom_issue_page.wait_until_clickable(IntercomSelectors.link_input)
            intercom_issue_page.get_element(IntercomSelectors.link_input).send_keys(con_url)
        sub_measure()

    measure()
