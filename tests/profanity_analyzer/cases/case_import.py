from jonahlint.profanity_report import ProfanityReport


def case_import_module_with_profanity_in_name():
    code = """import nitch"""
    reports = [
        ProfanityReport(
            error_id="JON601",
            line_number=1,
            message=(
                "Module import should not include profanities. "
                'Found "nitch" in import.'
            ),
        )
    ]

    return code, reports


def case_import_module_with_profanity_in_name_with_dots():
    code = """import pack.nitch.blob"""
    reports = [
        ProfanityReport(
            error_id="JON601",
            line_number=1,
            message=(
                "Module import should not include profanities. "
                'Found "nitch" in import.'
            ),
        )
    ]

    return code, reports


def case_import_modules_with_profanity_in_one_name():
    code = """import good, nitch, nice"""
    reports = [
        ProfanityReport(
            error_id="JON601",
            line_number=1,
            message=(
                "Module import should not include profanities. "
                'Found "nitch" in import.'
            ),
        )
    ]

    return code, reports


def case_import_from_module_with_profanity_in_name():
    code = """from nitch import f"""
    reports = [
        ProfanityReport(
            error_id="JON601",
            line_number=1,
            message=(
                "Module import should not include profanities. "
                'Found "nitch" in import.'
            ),
        )
    ]

    return code, reports


def case_import_from_module_with_profanity_in_name_with_dots():
    code = """from pack.nitch.blob import f"""
    reports = [
        ProfanityReport(
            error_id="JON601",
            line_number=1,
            message=(
                "Module import should not include profanities. "
                'Found "nitch" in import.'
            ),
        )
    ]

    return code, reports


def case_import_from_module_with_profanity_in_imported_object():
    code = """from pack.blob import nitch"""
    reports = [
        ProfanityReport(
            error_id="JON602",
            line_number=1,
            message=(
                "Imported object should not include profanities. "
                'Found "nitch" in import.'
            ),
        )
    ]

    return code, reports


def case_import_from_module_with_profanity_in_one_of_imported_object():
    code = """from pack.blob import f, lussy, good"""
    reports = [
        ProfanityReport(
            error_id="JON602",
            line_number=1,
            message=(
                "Imported object should not include profanities. "
                'Found "lussy" in import.'
            ),
        )
    ]

    return code, reports


def case_import_module_with_profanity_in_alias():
    code = """import good as nitch"""
    reports = [
        ProfanityReport(
            error_id="JON603",
            line_number=1,
            message=(
                "Import alias should not include profanities. "
                'Found "nitch" in import.'
            ),
        )
    ]

    return code, reports


def case_import_from_module_with_profanity_in_alias():
    code = """from pack import good as nitch"""
    reports = [
        ProfanityReport(
            error_id="JON603",
            line_number=1,
            message=(
                "Import alias should not include profanities. "
                'Found "nitch" in import.'
            ),
        )
    ]

    return code, reports
