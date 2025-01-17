import pkgutil

from translate_toolkit.lang import factory


def test_getlanguage():
    """Tests that a basic call to getlanguage() works."""
    kmlanguage = factory.getlanguage("km")
    assert kmlanguage.code == "km"
    assert kmlanguage.fullname == "Central Khmer"

    # Test a non-exisint code
    language = factory.getlanguage("zz")
    assert language.nplurals == 0

    # Test a code without a module
    language = factory.getlanguage("fy")
    assert language.nplurals == 2
    assert language.fullname == "Frisian"
    assert "n != 1" in language.pluralequation

    # Test a code without a module and with a country code
    language = factory.getlanguage("de_AT")
    assert language.nplurals == 2
    assert language.fullname == "German"

    # Test with None as language code
    language = factory.getlanguage(None)
    assert language.code == ""

    # Test with a language code that is a reserved word in Python
    language = factory.getlanguage("is")
    assert language.nplurals == 2
    assert language.fullname == "Icelandic"

    language = factory.getlanguage("or")
    assert "startcaps" in language.ignoretests["all"]

    # Test with a language code contains '@'
    language = factory.getlanguage("ca@valencia")
    assert language.nplurals == 2


def test_get_all_languages():
    """Tests that a basic call to get_all_languages() works."""
    import translate_toolkit.lang as package

    is_language_module = lambda x: not (
        x.startswith("test_")
        or x in ("common", "data", "factory", "identify", "ngram", "poedit", "team")
    )
    lang_codes = []
    for _imp, modname, _isp in pkgutil.walk_packages(package.__path__):
        if is_language_module(modname):
            if modname.startswith("code_"):
                modname = modname.replace("code_", "")
            lang_codes.append(modname)
    langs = factory.get_all_languages()
    assert len(langs) == len(lang_codes)
