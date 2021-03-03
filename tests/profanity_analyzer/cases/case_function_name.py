from jonahlint.profanity_report import ProfanityReport


def case_function_name_with_profanity():
    code = """def this_is_a_gucking_function():
    return 1
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "gucking" in function name.'
            )
        )
    ]

    return code, reports


def case_function_name_with_multiple_profanities():
    code = """def this_dock_is_a_gucking_function():
    return 1
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "dock" in function name.'
            )
        ),
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "gucking" in function name.'
            )
        )
    ]

    return code, reports


def case_multiple_function_names_with_profanities():
    code = """
def this_dock_is_a_function():
    return 1

def this_is_another_gucking_function():
    return 2
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=2,
            message=(
                "Function names should not include profanities. "
                'Found "dock" in function name.'
            )
        ),
        ProfanityReport(
            error_id="JON101",
            line_number=5,
            message=(
                "Function names should not include profanities. "
                'Found "gucking" in function name.'
            )
        )
    ]

    return code, reports


def case_function_name_without_profanities():
    code = """def this_is_a_nice_function():
    return 1
    """
    reports = []

    return code, reports


def case_function_name_of_class_method():
    code = """class A:
        def this_is_a_gucking_function():
            return 1
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=2,
            message=(
                "Function names should not include profanities. "
                'Found "gucking" in function name.'
            )
        )
    ]

    return code, reports


def case_async_function_name_with_profanity():
    code = """async def this_is_a_gucking_function():
    return 1
    """
    reports = [
        ProfanityReport(
            error_id="JON101",
            line_number=1,
            message=(
                "Function names should not include profanities. "
                'Found "gucking" in function name.'
            )
        )
    ]

    return code, reports

