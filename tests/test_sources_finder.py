from pathlib import Path

from pytest_cases import parametrize_with_cases

from jonahlint.sources_finder import SourcesFinder


def touched_path(path: Path):
    path.touch()
    return path


def case_base_is_a_source(tmpdir_factory):
    basedir = Path(tmpdir_factory.mktemp("base"))
    basedir.mkdir(parents=True, exist_ok=True)
    source = touched_path(basedir / "code.py")

    return source, [source]


def case_base_is_dir_with_one_source(tmpdir_factory):
    basedir = Path(tmpdir_factory.mktemp("base"))
    basedir.mkdir(parents=True, exist_ok=True)
    source = touched_path(basedir / "code.py")

    return basedir, [source]


def case_base_is_dir_with_two_sources(tmpdir_factory):
    basedir = Path(tmpdir_factory.mktemp("base"))
    basedir.mkdir(parents=True, exist_ok=True)
    source1 = touched_path(basedir / "code1.py")
    source2 = touched_path(basedir / "code2.py")

    return basedir, [source1, source2]


def case_base_is_dir_with_no_sources(tmpdir_factory):
    basedir = Path(tmpdir_factory.mktemp("base"))
    basedir.mkdir(parents=True, exist_ok=True)

    return basedir, []


def case_base_is_dir_with_no_python_files(tmpdir_factory):
    basedir = Path(tmpdir_factory.mktemp("base"))
    basedir.mkdir(parents=True, exist_ok=True)
    touched_path(basedir / "data1.txt")
    touched_path(basedir / "data2.json")

    return basedir, []


def case_base_is_dir_with_recursive_source(tmpdir_factory):
    base1 = Path(tmpdir_factory.mktemp("base"))
    inner = base1 / "inner1" / "inner2" / "inner3"
    inner.mkdir(parents=True, exist_ok=True)
    source = touched_path(inner / "code.py")

    return base1, [source]


@parametrize_with_cases(argnames=["base_path", "expected_sources"], cases=".")
def test_finds_sources(base_path, expected_sources):
    assert SourcesFinder.find_sources(base_path) == expected_sources
