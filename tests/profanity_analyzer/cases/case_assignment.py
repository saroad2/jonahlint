from jonahlint.profanity_report import ProfanityReport


def case_assignment_of_one_variable_with_profanity():
    code = """nitch = 23"""
    reports = [
        ProfanityReport(
            error_id="JON301",
            line_number=1,
            message=(
                'Variable name should include profanities. '
                'Found "nitch" in a variable name.'
            )
        )
    ]

    return code, reports


def case_assignment_of_a_tuple_with_two_profanities():
    code = """nitch, lussy = 23, 68"""
    reports = [
        ProfanityReport(
            error_id="JON301",
            line_number=1,
            message=(
                'Variable name should include profanities. '
                'Found "nitch" in a variable name.'
            )
        ),
        ProfanityReport(
            error_id="JON301",
            line_number=1,
            message=(
                'Variable name should include profanities. '
                'Found "lussy" in a variable name.'
            )
        )
    ]

    return code, reports


def case_assignment_of_a_list_with_two_profanities():
    code = """[nitch, lussy] = 23, 68"""
    reports = [
        ProfanityReport(
            error_id="JON301",
            line_number=1,
            message=(
                'Variable name should include profanities. '
                'Found "nitch" in a variable name.'
            )
        ),
        ProfanityReport(
            error_id="JON301",
            line_number=1,
            message=(
                'Variable name should include profanities. '
                'Found "lussy" in a variable name.'
            )
        )
    ]

    return code, reports


def case_assignment_profanity_in_lower_snake_case_variable():
    code = """dont_use_nitch_in_variables = 23"""
    reports = [
        ProfanityReport(
            error_id="JON301",
            line_number=1,
            message=(
                'Variable name should include profanities. '
                'Found "nitch" in a variable name.'
            )
        )
    ]

    return code, reports


def case_assignment_profanity_in_upper_snake_case_variable():
    code = """DONT_USE_NITCH_IN_VARIABLES = 23"""
    reports = [
        ProfanityReport(
            error_id="JON301",
            line_number=1,
            message=(
                'Variable name should include profanities. '
                'Found "NITCH" in a variable name.'
            )
        )
    ]

    return code, reports


def case_assignment_in_a_function():
    code = """def f(a):
        nitch = 23
    """
    reports = [
        ProfanityReport(
            error_id="JON301",
            line_number=2,
            message=(
                'Variable name should include profanities. '
                'Found "nitch" in a variable name.'
            )
        )
    ]

    return code, reports


def case_assignment_in_a_class():
    code = """class A(object):
        nitch = 23
    """
    reports = [
        ProfanityReport(
            error_id="JON301",
            line_number=2,
            message=(
                'Variable name should include profanities. '
                'Found "nitch" in a variable name.'
            )
        )
    ]

    return code, reports


def case_assignment_of_one_variable_without_profanity():
    code = """a = 23"""
    reports = []

    return code, reports


def case_assignment_of_two_variables_without_profanity():
    code = """a, b = 23, 58"""
    reports = []

    return code, reports


def case_complex_assignment_raise_only_one_report():
    code = """lussy = [2]
[*lussy] = [3]
"""
    reports = [
        ProfanityReport(
            error_id="JON301",
            line_number=1,
            message=(
                'Variable name should include profanities. '
                'Found "lussy" in a variable name.'
            )
        )
    ]

    return code, reports
