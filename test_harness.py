from AAAPT.runner import register_tests

test_suites = {
    'card_options': ['Trello.tests.test_card_options'],
    'executable'  : ['Trello.tests.test_executable'],
    'operations'  : ['Trello.tests.test_operations'],
    'output'      : ['Trello.tests.test_output']
}

register_tests(test_suites)