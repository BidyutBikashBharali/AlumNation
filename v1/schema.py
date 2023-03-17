from pydantic import BaseModel, Field, validator, EmailStr, constr, AnyHttpUrl
from datetime import datetime, date



class UserBaseSchema(BaseModel):
    name: str = Field(default="")
    email: EmailStr
    ph_no : str = Field(default="0123456789", min_length=10, max_length=10)
    # photo: str
    role: str | None = Field(default="")
    address: str = Field(default="")
    about_me: str = Field(default="")
    fb: str = Field(default="")
    insta: str = Field(default="")
    git: str = Field(default="")
    linked: str = Field(default="")
    branch:str = Field(default="")
    institute:str = Field(default="")
    passout_year:str = Field(default="")
    isAlumni: bool = Field(default=False)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class UserUpdateSchema(UserBaseSchema):
    password: str | None = None
    passwordConfirm: str | None = None

    










class AdminBaseSchema(BaseModel):
    name: str = Field(default="")
    email: EmailStr
    ph_no : str = Field(default="0123456789", min_length=10, max_length=10)
    # photo: str
    role: str | None = Field(default="")
    address: str = Field(default="")
    about_me: str = Field(default="")
    fb: str = Field(default="")
    insta: str = Field(default="")
    git: str = Field(default="")
    linked: str = Field(default="")
    branch:str = Field(default="")
    institute:str = Field(default="")
    passout_year:str = Field(default="")
    isAlumni: bool = Field(default=False)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreateAdminSchema(AdminBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False


class LoginAdminSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class AdminResponseSchema(AdminBaseSchema):
    id: str
    pass


class AdminResponse(BaseModel):
    status: str
    admin: AdminResponseSchema


class AdminUpdateSchema(AdminBaseSchema):
    password: str | None = None
    passwordConfirm: str | None = None






class PostBaseSchema(BaseModel):
    title: str | None = None
    content: str
    media_url: AnyHttpUrl = Field(default="http://example1.com")
    created_by: EmailStr
    name: str
    role: str | None = Field(default="")
    created_at: datetime | None = None
    updated_at: datetime | None = None
    


class PostUpdateSchema(PostBaseSchema):
    pass


class EmailSchema(BaseModel):
    email_from: EmailStr = Field(default="dev.acc.4.exprmnt@gmail.com")
    email_to: list[EmailStr] = Field(default=["roy4suraj@gmail.com", "bidyutbikashbharali6@gmail.com"])
    subject: str | None = Field(default="This Is Just A Default Subject, You Can Add Your Own")
    content:str | None = Field(default="This is just a default content, replace it with your own")