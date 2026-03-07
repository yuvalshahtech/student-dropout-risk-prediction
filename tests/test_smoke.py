def test_package_import_and_version():
    import student_management

    assert student_management.__version__ == "1.6.0"


def test_main_entry_importable():
    import student_management.__main__ as main_mod

    assert hasattr(main_mod, "main")
