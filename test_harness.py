from AAAPT.runner import register_tests

test_suites = {
    'card_options': ['Trello.tests.test_card_options'],
    'navigator': ['Trello.tests.test_navigator']
}

register_tests(test_suites)