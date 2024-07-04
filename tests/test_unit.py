from Employee.models import Employees
def test_new_employee():
    employee = Employees(name="Akshith", department = "software")
    assert employee.name == "Akshith"
    assert employee.department == "software"