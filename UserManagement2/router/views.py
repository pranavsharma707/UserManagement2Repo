from fastapi import APIRouter,status,HTTPException
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from models import Organization,Tenant,Role,TenantUser
import models
from settings import get_db
from schema import User ,userRole
from password_generator import PasswordGenerator

import uuid


def id_uuids():
    uid=uuid.uuid4()
    id_uid=str(uid)
    print(type(id_uid))
    return id_uid
def randoms():
    pwo = PasswordGenerator()
    pwo.minlen = 8  # (Optional)
    pwo.maxlen = 8  # (Optional)
    pwo.minuchars = 2  # (Optional)
    pwo.minlchars = 3  # (Optional)
    pwo.minnumbers = 1  # (Optional)
    pwo.minschars = 1  # (Optional)

    password_string=pwo.generate()
    return password_string
router=APIRouter()


@router.post('/role/',status_code=status.HTTP_200_OK)
def create_role(request:userRole, db: Session = Depends(get_db)):
    id_uid = id_uuids()
    role = Role(id=id_uid, name=request.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.post('/userRegisteration/',status_code=status.HTTP_201_CREATED)
def userRegisteration(request:User,db:Session=Depends(get_db)):

    id_uid=id_uuids()
    organization=Organization(id=id_uid,name=request.organization_name)
    db.add(organization)
    db.commit()
    db.refresh(organization)

    id_uid = id_uuids()
    tenant=Tenant(id=id_uid, name=request.tenant_name, company_logo=request.company_logo, organization_id=organization.id)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    role = db.query(models.Role).filter(models.Role.name == "tenentAdmin").first()
    if role:
        print(role.id)

    else:

        role = Role(id=id_uid, name="tenentAdmin")
        db.add(role)
        db.commit()
        db.refresh(role)

        # atuo generate password
    a = randoms()
    password = str(a)
    Tenantuser = TenantUser(id=id_uid, username=request.username,
                        role_id=role.id, password=password,
                        tenant_id=tenant.id)
    db.add(Tenantuser)
    db.commit()
    db.refresh(Tenantuser)

    return {organization, tenant, Tenantuser}


@router.get('/tentant_user_data/{id}',status_code=status.HTTP_302_FOUND)
def get_data(id:str,db: Session = Depends(get_db)):
    user=db.query(TenantUser).filter(TenantUser.id==id).first()
    return user


@router.put('/update/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:str,request:User,db:Session=Depends(get_db)):
    tenantuser=db.query(TenantUser).filter(TenantUser.id==id)
    if not tenantuser.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'TenantUser with id {id} is not available')     
    tenantuser.update({'username':request.username,'first_name':request.firstname,'last_name':request.lastname,'email':request.email,'password':request.password,'account_name':request.account_name,
    'title':request.title,'country':request.country,'line_manager':request.line_manager,'address':request.address,'department':request.department,'job_title':request.job_title,'date_of_birth':request.date_of_birth,
    'start_date':request.start_date,'town':request.town,'postcode':request.postcode,'cell_number':request.cell_number,'level_twomanager':request.level_twomanager})
    db.commit()
    return 'updated'






@router.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id,db:Session=Depends(get_db)):
    tenantuser=db.query(TenantUser).filter(TenantUser.id==id)
    if not tenantuser.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'TenantUser with id {id} is not available')
    tenantuser.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.get('/get_role/{id}',status_code=status.HTTP_302_FOUND)
def get_data(id:str,db: Session = Depends(get_db)):
    role=db.query(Role).filter(Role.id==id).first()
    return role

    
@router.put('/role_update/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:str,request:userRole,db:Session=Depends(get_db)):
    role=db.query(Role).filter(Role.id==id)
    if not role.first():
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Role with id {id} is not available')
    role.update({'name':request.name})     
    db.commit()
    return 'updated'


@router.delete('/role_delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id:str,db:Session=Depends(get_db)):
    role=db.query(Role).filter(Role.id==id)
    if not role.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Role with id {id} is not available')
    role.delete(synchronize_session=False)
    db.commit()
    return 'done'





    




