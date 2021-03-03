from jonahlint.profanity_report import ProfanityReport


def case_function_profane_parameter_name():
    code = """def f(gucking_parameter):
    return gucking_parameter + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function parameter names should not include profanities. "
                'Found "gucking" in the name of a parameter of the function "f".'
            )
        )
    ]

    return code, reports


def case_function_two_profane_parameter_names():
    code = """def f(gucking_parameter, dock):
    return gucking_parameter + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function parameter names should not include profanities. "
                'Found "gucking" in the name of a parameter of the function "f".'
            )
        ),
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function parameter names should not include profanities. "
                'Found "dock" in the name of a parameter of the function "f".'
            )
        )
    ]

    return code, reports


def case_function_profane_parameter_name_with_annotation():
    code = """def f(gucking_parameter: float):
    return gucking_parameter + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function parameter names should not include profanities. "
                'Found "gucking" in the name of a parameter of the function "f".'
            )
        )
    ]

    return code, reports


def case_function_profane_parameter_name_with_default_value():
    code = """def f(gucking_parameter = 5):
    return gucking_parameter + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function parameter names should not include profanities. "
                'Found "gucking" in the name of a parameter of the function "f".'
            )
        )
    ]

    return code, reports


def case_function_one_profane_parameter_from_multiple():
    code = """def f(a, dock, c):
    return dock * (a + c)
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function parameter names should not include profanities. "
                'Found "dock" in the name of a parameter of the function "f".'
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
                "Function parameter names should not include profanities. "
                'Found "gucking" in the name of a parameter of the function "f".'
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
                "Function parameter names should not include profanities. "
                'Found "gucking" in the name of a parameter of the function "f".'
            )
        ),
    ]

    return code, reports


def case_method_function_profane_parameter_name():
    code = """class A:
        def f(gucking_parameter):
            return gucking_parameter + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=2,
            message=(
                "Function parameter names should not include profanities. "
                'Found "gucking" in the name of a parameter of the function "f".'
            )
        )
    ]

    return code, reports


def case_async_function_profane_parameter_name():
    code = """async def f(gucking_parameter):
    return gucking_parameter + 1
    """
    reports = [
        ProfanityReport(
            error_id="JON102",
            line_number=1,
            message=(
                "Function parameter names should not include profanities. "
                'Found "gucking" in the name of a parameter of the function "f".'
            )
        )
    ]

    return code, reports
