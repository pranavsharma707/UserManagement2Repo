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


@router.put('/update/{id}',status_code=status.HTTP_302_FOUND)
def update_all(id:str,request:User,db:Session=Depends(get_db)):
    data=id
    organization=db.query(Organization).filter(Organization.id==data)
    organization.update({'name':request.organization_name})
    terrant=db.query(Tenant).filter(Tenant.organization_id==data)
    terrant.update({'name':request.tenant_name,'company_logo':request.company_logo})
    db.commit()
    terrant_user=db.query(TenantUser).filter(TenantUser.id==terrant.id)
    terrant_user.update({'username':request.username,'first_name':request.firstname,'last_name':request.lastname,'email':request.email,'password':request.password,'account_name':request.account_name,
    'title':request.title,'country':request.country,'line_manager':request.line_manager,'address':request.address,'department':request.department,'job_title':request.job_title,'date_of_birth':request.date_of_birth,
    'start_date':request.start_date,'town':request.town,'postcode':request.postcode,'cell_number':request.cell_number,'level_twomanager':request.level_twomanager})
    db.commit()
    return 'update successfully'


    














