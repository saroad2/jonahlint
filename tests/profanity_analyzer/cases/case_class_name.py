from jonahlint.profanity_report import ProfanityReport


def case_class_name_is_title_profanity():
    code = """class Nitch:
    pass
    """
    reports = [
        ProfanityReport(
            error_id="JON201",
            line_number=1,
            message=(
                "Class names should not include profanities. "
                'Found "Nitch" in class name.'
            ),
        )
    ]

    return code, reports


def case_class_name_with_profanity():
    code = """class ThisIsAGuckingClass:
    pass
    """
    reports = [
        ProfanityReport(
            error_id="JON201",
            line_number=1,
            message=(
                "Class names should not include profanities. "
                'Found "Gucking" in class name.'
            ),
        )
    ]

    return code, reports


def case_class_name_with_multiple_profanities():
    code = """class ThisDockIsAGuckingClass:
    pass
    """
    reports = [
        ProfanityReport(
            error_id="JON201",
            line_number=1,
            message=(
                "Class names should not include profanities. "
                'Found "Dock" in class name.'
            ),
        ),
        ProfanityReport(
            error_id="JON201",
            line_number=1,
            message=(
                "Class names should not include profanities. "
                'Found "Gucking" in class name.'
            ),
        ),
    ]

    return code, reports


def case_multiple_class_names_with_profanities():
    code = """
class ThisDockIsAClass:
    pass

class ThisIsAnotherGuckingClass:
    pass
    """
    reports = [
        ProfanityReport(
            error_id="JON201",
            line_number=2,
            message=(
                "Class names should not include profanities. "
                'Found "Dock" in class name.'
            ),
        ),
        ProfanityReport(
            error_id="JON201",
            line_number=5,
            message=(
                "Class names should not include profanities. "
                'Found "Gucking" in class name.'
            ),
        ),
    ]

    return code, reports


def case_class_name_without_profanities():
    code = """class ThisIsANiceClass:
    pass
    """
    reports = []

    return code, reports
