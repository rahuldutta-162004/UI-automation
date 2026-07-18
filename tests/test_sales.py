from pytest_bdd import scenario
from qase.pytest import qase

from steps.sales_steps import *

@qase.id(1)
@scenario("../features/sales.feature")
def test_saved_sales_order():
    pass
