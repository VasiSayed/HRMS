function filterdept() {
  const dept_choice = document.getElementById("departmeeeeeent").value;
  const employeees = document.querySelectorAll(".empname");
  console.log(employeees);
  employeees.forEach((emp) => {
    const emp_dept = emp.getAttribute("data-department");
    if (emp_dept === dept_choice) {
      emp.style.display = "table-row";
    } else {
      emp.style.display = "none";
    }
  });
}
