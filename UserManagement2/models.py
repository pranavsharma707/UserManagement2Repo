from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from settings import Base
import datetime
import pytz


class Organization(Base):

    __tablename__ = "organization"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    tenant = relationship("Tenant", back_populates="tenant")


class Tenant(Base):

    __tablename__ = "tenant"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    company_logo = Column(String)
    organization_id = Column(String, ForeignKey('organization.id', ondelete='SET NULL'), nullable=True)
    created_date = Column(DateTime,default=datetime.datetime.now(pytz.timezone('Asia/Dubai')))
    updated_date = Column(DateTime,default=datetime.datetime.now(pytz.timezone('Asia/Dubai')))
    tenant_group = relationship("Group", back_populates="tenant_group")
    tenant_user= relationship("TenantUser", back_populates="tenant_user")
    tenant = relationship("Organization", back_populates="tenant")


class Group(Base):

    __tablename__ = "group"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    tenant_id = Column(String, ForeignKey('tenant.id', ondelete='SET NULL'), nullable=True)
    group_id=Column(String, ForeignKey('group.id'))
    created_date = Column(DateTime,default=datetime.datetime.now(pytz.timezone('Asia/Dubai')))
    updated_date = Column(DateTime,default=datetime.datetime.now(pytz.timezone('Asia/Dubai')))
    group = relationship("Group")
    tenant_group = relationship("Tenant", back_populates="tenant_group")
    group_user = relationship("GroupUsers", back_populates="group_user")



class Role(Base):

    __tablename__ = "role"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    role = relationship("TenantUser", back_populates="role")

#done
class TenantUser(Base):

    __tablename__ = "tenantUser"

    id = Column(String, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    account_name = Column(String)
    title = Column(String)
    country=Column(String)
    line_manager=Column(String)
    address=Column(String)
    department=Column(String)
    job_title=Column(String)
    date_of_birth=Column(String)
    start_date=Column(String)
    town=Column(String)
    postcode=Column(String)
    cell_number = Column(String)
    level_twomanager = Column(String)

    role_id = Column(String, ForeignKey('role.id', ondelete='SET NULL'), nullable=True)
    tenant_id = Column(String, ForeignKey('tenant.id', ondelete='SET NULL'), nullable=True)
    created_date = Column(DateTime,default=datetime.datetime.now(pytz.timezone('Asia/Dubai')))
    updated_date = Column(DateTime,default=datetime.datetime.now(pytz.timezone('Asia/Dubai')))
    tenant_user = relationship("Tenant", back_populates="tenant_user")
    tenant_group = relationship("GroupUsers", back_populates="tenant_group")
    role = relationship("Role", back_populates="role")





class GroupUsers(Base):

    __tablename__= "groupUser"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('tenantUser.id', ondelete='SET NULL'), nullable=True)
    group_id = Column(String, ForeignKey('group.id', ondelete='SET NULL'), nullable=True)
    group_user = relationship("Group", back_populates="group_user")
    tenant_group = relationship("TenantUser", back_populates="tenant_group")