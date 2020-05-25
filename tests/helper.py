from unittest import mock


def get_mocked_subprocess_popen():
    """Get a mocked subprocess popen for testing

    Returns:
        Mock -- mock to be used
    """
    process_mock = mock.Mock()
    attrs = {"communicate.return_value": ("output", "error")}
    process_mock.configure_mock(**attrs)
    return process_mock
