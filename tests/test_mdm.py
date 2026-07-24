from pytest_bdd import scenario
from qase.pytest import qase

@qase.id(101)
@scenario("../features/mdm.feature", "Edit and verify item description from MDM task")
def test_edit_item_description():
    pass


@qase.id(102)
@scenario("../features/mdm.feature", "Edit configuration code and validate that it can't be editable")
def test_edit_configuration_code():
    pass
