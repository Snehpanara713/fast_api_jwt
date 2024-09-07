from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session


from api.employee.model import Employee

from api.employee.employee_schema import (
    emoloyee_schemas,
    emoloyee_schemas_update,
    modify_emoloyee_schemas_update,
)
from werkzeug.security import generate_password_hash, check_password_hash


from comman.comman_model import SuccessResponse

from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash


from db.database import get_db

employee = APIRouter()


@employee.post("/")
def signup_employee(emp_data: emoloyee_schemas, db: Session = Depends(get_db)):
    try:

        existing_employee = (
            db.query(Employee).filter(Employee.email == emp_data.email).first()
        )
        if existing_employee:
            return SuccessResponse(
                hasError=True, statusCode=500, errorMsg="Email already registered"
            )

        employee = Employee(
            first_name=emp_data.first_name,
            last_name=emp_data.last_name,
            phone=emp_data.phone,
            email=emp_data.email,
            password=generate_password_hash(emp_data.password),
            Role=emp_data.Role,
            Date_of_birth=emp_data.Date_of_birth,
        )

        db.add(employee)
        db.commit()

        response = SuccessResponse(
            hasError=False,
            statusCode=200,
            result={
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
                # "password": employee.password,
                "Role": employee.Role,
                "phone": employee.phone,
                "Date_of_birth": employee.Date_of_birth,
            },
        )

    except Exception as e:
        return SuccessResponse(hasError=True, statusCode=500, errorMsg=str(e))

    return response


@employee.post("/login")
def login(
    email: str,
    password: str,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    try:
        emp = db.query(Employee).filter(Employee.email == email).first()

        if employee and check_password_hash(emp.password, password):
            access_token = Authorize.create_access_token(subject=emp.emp_id)
            refresh_token = Authorize.create_refresh_token(subject=emp.emp_id)

            response = SuccessResponse(
                hasError=False,
                statusCode=200,
                # "message":"You have successfully logged in"
                result={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    # "message": "You have successfully logged in",
                },
            )

        else:
            return SuccessResponse(
                hasError=True,
                statusCode=status.HTTP_400_BAD_REQUEST,
                errorMsg="Invalid Email Or Password",
            )

    except Exception as e:
        return SuccessResponse(hasError=True, statusCode=500, errorMsg=str(e))

    return response


@employee.get("/get_employee")
def get_employee_search(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:

        try:
            Authorize.jwt_required()
        except Exception as e:
            return SuccessResponse(
                hasError=True,
                statusCode=status.HTTP_401_UNAUTHORIZED,
                errorMsg="Invalid Token",
            )
        data = db.query(Employee).all()

        list = []

        if data:
            for employee in data:
                list.append(
                    {
                        "emp_id": employee.emp_id,
                        "first_name": employee.first_name,
                        "last_name": employee.last_name,
                        "email": employee.email,
                        # "password": employee.password,
                        "phone": employee.phone,
                        "role": employee.Role,
                        "Date_of_birth": employee.Date_of_birth,
                    }
                )

            response = SuccessResponse(hasError=False, statusCode=200, result=list)
        else:
            response = SuccessResponse(
                hasError=True, statusCode=404, errorMsg="No data found"
            )

    except Exception as e:
        db.rollback()
        response = SuccessResponse(hasError=True, statusCode=500, errorMsg=str(e))

    return response


@employee.get("/search")
def get_employee_search(
    page: int = 1,
    page_size: int = 10,
    search: str = "",
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:

        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token",
            )
        query = (
            db.query(Employee)
            .filter(Employee.first_name.like(f"%{search}%"))
            .filter(Employee.last_name.like(f"%{search}%"))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        data = query.all()
        total_count = (
            db.query(Employee)
            .filter(Employee.first_name.like(f"%{search}%"))
            .filter(Employee.last_name.like(f"%{search}%"))
            .count()
        )

        list = []

        if data:
            for employee in data:
                list.append(
                    {
                        "emp_id": employee.emp_id,
                        "first_name": employee.first_name,
                        "last_name": employee.last_name,
                        "email": employee.email,
                        # "password": employee.password,
                        "phone": employee.phone,
                        "role": employee.Role,
                        "Date_of_birth": employee.Date_of_birth,
                    }
                )

            response = SuccessResponse(
                hasError=False,
                statusCode=200,
                result={
                    "data": list,
                    "total_count": total_count,
                    "page_no": page,
                    "page_size": page_size,
                },
            )
        else:
            response = SuccessResponse(
                hasError=True, statusCode=404, errorMsg="No data found"
            )

    except Exception as e:
        db.rollback()
        response = SuccessResponse(hasError=True, statusCode=500, errorMsg=str(e))

    return response


@employee.get("/{emp_id}")
def get_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token",
            )

        emp_data = db.query(Employee).filter(Employee.emp_id == emp_id).first()

        if emp_data:
            data = {
                "emp_id": emp_data.emp_id,
                "first_name": emp_data.first_name,
                "last_name": emp_data.last_name,
                "email": emp_data.email,
                "phone": emp_data.phone,
                "role": emp_data.Role,
                "Date_of_birth": emp_data.Date_of_birth,
            }

            response = SuccessResponse(hasError=False, statusCode=200, result=data)
        else:
            response = SuccessResponse(
                hasError=True, statusCode=404, errorMsg="Data not found"
            )

    except Exception as e:
        db.rollback()
        response = SuccessResponse(hasError=True, statusCode=500, errorMsg=str(e))

    return response.dict()


@employee.delete("/{emp_id}/employee_data")
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:

        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token",
            )
        u = db.query(Employee).filter(Employee.emp_id == emp_id).first()
        if u:
            db.delete(u)
            db.commit()

            response = SuccessResponse(
                hasError=False, statusCode=200, result={"delete": emp_id}
            )
        else:
            response = SuccessResponse(
                hasError=True,
                statusCode=404,
                errorMsg=f"Employee id {emp_id} not found",
            )

    except Exception as e:
        db.rollback()
        response = SuccessResponse(hasError=True, statusCode=500, errorMsg=str(e))

    return response


@employee.put("/update_employee")
def update_employee_data(
    emp_id: int,
    emp: emoloyee_schemas_update,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:
        try:
            Authorize.jwt_required()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token",
            )
        d = db.query(Employee).filter(Employee.emp_id == emp_id).first()

        if d:
            d.first_name = (emp.first_name,)
            d.last_name = (emp.last_name,)
            d.email = (emp.email,)
            d.phone = (emp.phone,)
            d.Role = (emp.Role,)
            d.Date_of_birth = (emp.Date_of_birth,)

            db.add(d)
            db.commit()
            db.refresh(d)

            response = SuccessResponse(
                hasError=False,
                statusCode=200,
                result={
                    "first_name": d.first_name,
                    "last_name": d.last_name,
                    "email": d.email,
                    "phone": d.phone,
                    "Role": d.Role,
                    "Date_of_birth": d.Date_of_birth,
                    "emp_id": d.emp_id,
                },
            )
        else:
            response = SuccessResponse(
                hasError=True, statusCode=404, errorMsg="State not found"
            )

    except Exception as e:
        db.rollback()
        response = SuccessResponse(hasError=True, statusCode=500, errorMsg=str(e))

    return response


@employee.patch("/{emp_id} ")
async def update_employee(
    emp_id: int,
    employee: modify_emoloyee_schemas_update,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:
        # Ensure valid token
        Authorize.jwt_required()

        # Check if employee exists
        stored_employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()

        if not stored_employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Extract fields to update from request data
        update_data = employee.dict(exclude_unset=True)

        # Update fields in stored_employee
        for key, value in update_data.items():
            setattr(stored_employee, key, value)

        db.add(stored_employee)  # Add the updated employee object to the session
        db.commit()  # Commit the transaction
        db.refresh(stored_employee)  # Refresh the stored employee instance from the DB

        # Prepare the success response
        response = SuccessResponse(
            hasError=False,
            statusCode=200,
            result={
                "first_name": stored_employee.first_name,
                "last_name": stored_employee.last_name,
                "email": stored_employee.email,
                "phone": stored_employee.phone,
                "Role": stored_employee.Role,
                "Date_of_birth": stored_employee.Date_of_birth,
                "emp_id": stored_employee.emp_id,
            },
        )

    except Exception as e:
        # Rollback in case of any exception
        db.rollback()
        response = SuccessResponse(hasError=True, statusCode=500, errorMsg=str(e))

    return response
