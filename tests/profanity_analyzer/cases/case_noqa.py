from jonahlint.profanity_report import ProfanityReport


def case_ignore_profanity_in_assignment():
    code = """nitch = 23  # noqa: JON301"""
    reports = []

    return code, reports


def case_ignore_profanity_in_function_name():
    code = """def nitch(a):  # noqa: JON101
    pass
    """
    reports = []

    return code, reports


def case_ignore_multiple_profanities_in_one_line():
    code = """def nitch(lussy):  # noqa: JON101, JON102
    pass
    """
    reports = []

    return code, reports


def case_ignore_catch_only_one_profanity():
    code = """def nitch(lussy):  # noqa: JON102
    pass
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "nitch" in function name.'
            )
        )
    ]

    return code, reports


def case_noqa_comment_on_wrong_line():
    code = """def nitch(a):
    pass  # noqa: JON101
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "nitch" in function name.'
            )
        )
    ]

    return code, reports
