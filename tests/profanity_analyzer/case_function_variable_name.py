from jonahlint.profanity_report import ProfanityReport


def case_function_profane_variable_name():
    code = """def f(gucking_variable):
    return gucking_variable + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function variable names should not include profanities. "
                'Found "gucking" in the name of a variable of the function "f".'
            )
        )
    ]

    return code, reports


def case_function_two_profane_variable_names():
    code = """def f(gucking_variable, dock):
    return gucking_variable + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function variable names should not include profanities. "
                'Found "gucking" in the name of a variable of the function "f".'
            )
        ),
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function variable names should not include profanities. "
                'Found "dock" in the name of a variable of the function "f".'
            )
        )
    ]

    return code, reports


def case_function_profane_variable_name_with_annotation():
    code = """def f(gucking_variable: float):
    return gucking_variable + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function variable names should not include profanities. "
                'Found "gucking" in the name of a variable of the function "f".'
            )
        )
    ]

    return code, reports


def case_function_profane_variable_name_with_default_value():
    code = """def f(gucking_variable = 5):
    return gucking_variable + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function variable names should not include profanities. "
                'Found "gucking" in the name of a variable of the function "f".'
            )
        )
    ]

    return code, reports


def case_function_one_profane_variable_from_multiple():
    code = """def f(a, dock, c):
    return dock * (a + c)
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function variable names should not include profanities. "
                'Found "dock" in the name of a variable of the function "f".'
            )
        ),
    ]

    return code, reports


def case_profane_expended_arg():
    code = """def f(*gucking_list):
    return sum(gucking_list)
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function variable names should not include profanities. "
                'Found "gucking" in the name of a variable of the function "f".'
            )
        ),
    ]

    return code, reports


def case_profane_expended_kwarg():
    code = """def f(**gucking_dict):
    return sum(gucking_dict.values())
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function variable names should not include profanities. "
                'Found "gucking" in the name of a variable of the function "f".'
            )
        ),
    ]

    return code, reports
