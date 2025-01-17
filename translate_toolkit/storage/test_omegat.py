from pytest import mark

from translate_toolkit.storage import omegat as ot
from translate_toolkit.storage import test_base


class TestOtUnit(test_base.TestTranslationUnit):
    UnitClass = ot.OmegaTUnit


class TestOtFile(test_base.TestTranslationStore):
    StoreClass = ot.OmegaTFile

    @mark.xfail(
        reason="This doesn't work, due to two store classes handling different "
        "extensions, but factory listing it as one supported file type"
    )
    def test_extensions(self):
        assert False
