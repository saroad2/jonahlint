from jonahlint.profanity_report import ProfanityReport


def case_profane_comment():
    code = """a = 2 #  nitch!"""
    reports = [
        ProfanityReport(
            error_id="JON501",
            line_number=1,
            message=(
                "Comments should not contain profanities. "
                'Found "nitch" in a comment.'
            )
        )
    ]

    return code, reports


def case_comment_with_two_profanities():
    code = """a = 2 #  this is lussy nitch"""
    reports = [
        ProfanityReport(
            error_id="JON501",
            line_number=1,
            message=(
                "Comments should not contain profanities. "
                'Found "lussy" in a comment.'
            )
        ),
        ProfanityReport(
            error_id="JON501",
            line_number=1,
            message=(
                "Comments should not contain profanities. "
                'Found "nitch" in a comment.'
            )
        )
    ]

    return code, reports
