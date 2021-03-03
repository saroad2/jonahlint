from jonahlint.profanity_report import ProfanityReport


def case_constant_is_a_profanity():
    code = """print("nitch")"""
    reports = [
        ProfanityReport(
            error_id="JON401",
            line_number=1,
            message=(
                "Constant value should not include profanities. "
                'Found "nitch" in constant "nitch".'
            )
        )
    ]

    return code, reports


def case_constant_is_a_sentence_with_profanity():
    code = """print("Do not use nitch in your code!")"""
    reports = [
        ProfanityReport(
            error_id="JON401",
            line_number=1,
            message=(
                "Constant value should not include profanities. "
                'Found "nitch" in constant "Do not use nitch in your code!".'
            )
        )
    ]

    return code, reports


def case_constant_assignment_is_a_profanity():
    code = """a = 'nitch'"""
    reports = [
        ProfanityReport(
            error_id="JON401",
            line_number=1,
            message=(
                "Constant value should not include profanities. "
                'Found "nitch" in constant "nitch".'
            )
        )
    ]

    return code, reports


def case_constant_is_not_a_profanity():
    code = """print('nice!')"""
    reports = []

    return code, reports
