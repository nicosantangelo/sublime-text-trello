from AAAPT.runner import register_tests

test_suites = {
    'card_options': ['Trello.tests.test_card_options'],
    'navigate': ['Trello.tests.test_navigate']
}

register_tests(test_suites)