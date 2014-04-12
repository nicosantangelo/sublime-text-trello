try:
    from AAAPT.runner import register_tests
    register_tests({
        'card_options': ['Trello.tests.test_card_options'],
        'executable'  : ['Trello.tests.test_executable'],
        'operations'  : ['Trello.tests.test_operations'],
        'output'      : ['Trello.tests.test_output']
    })
except ImportError:
    print("Install the AAAPT Package to test Trello from SublimeText")
    