# user.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.database import SessionLocal
from app.auth_dep import get_current_employee
from app.oauth import create_access_token

router = APIRouter(tags=["Employees"])

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Employee registration
@router.post("/register", response_model=schemas.ShowEmployee)
def register_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(models.Employee).filter(models.Employee.email == employee.email).first():
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    hashed = utils.hash_password(employee.password)
    emp = models.Employee(
        name=employee.name,
        email=employee.email,
        phone=employee.phone,
        password=hashed,
        access_type=employee.access_type,
        token_type=employee.token_type,
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

# 2. Employee login and JWT token generation
@router.post("/login")
def login(emp_login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.email == emp_login.username).first()
    if not emp or not utils.verify_password(emp_login.password, emp.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"employee_id": emp.id})
    return {"access_token": token, "token_type": "bearer"}

# 3. Get all employees (JWT token required)
@router.get("/employees", response_model=list[schemas.ShowEmployee])
def get_all_employees(db: Session = Depends(get_db), current_emp: int = Depends(get_current_employee)):
    return db.query(models.Employee).all()

# 4. Get current employee's details (via JWT token)
@router.get("/employee/me", response_model=schemas.ShowEmployee)
def get_my_employee(db: Session = Depends(get_db), current_emp: int = Depends(get_current_employee)):
    emp = db.query(models.Employee).get(current_emp)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

# 5. Update current employee's details (via JWT token)
@router.put("/employee/update")
def update_my_employee(updates: schemas.UpdateEmployee, db: Session = Depends(get_db), current_emp: int = Depends(get_current_employee)):
    emp = db.query(models.Employee).get(current_emp)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if updates.name:        emp.name = updates.name
    if updates.phone:       emp.phone = updates.phone
    if updates.password:    emp.password = utils.hash_password(updates.password)
    if updates.access_type: emp.access_type = updates.access_type
    if updates.token_type:  emp.token_type = updates.token_type
    
    db.commit()
    return {"message": "Employee successfully updated"}

# 6. Delete current employee (via JWT token)
@router.delete("/employee/delete")
def delete_my_employee(db: Session = Depends(get_db), current_emp: int = Depends(get_current_employee)):
    emp = db.query(models.Employee).get(current_emp)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(emp)
    db.commit()
    return {"message": f"Employee with ID {current_emp} has been deleted"}
