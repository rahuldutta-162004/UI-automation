from pytest_bdd import scenario
from qase.pytest import qase

@qase.id(101)
@scenario("../features/mdm.feature", "Edit and verify item description from MDM task")
def test_create_customer():
    pass


@qase.id(102)
@scenario("../features/mdm.feature", "Edit configuration code and validate that it can't be editable")
def test_delete_customer():
    pass
