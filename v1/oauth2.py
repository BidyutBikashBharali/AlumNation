import base64
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from bson.objectid import ObjectId

from .serializers import userEntity, adminEntity #employeeEntity, adminEntity

from .database import cnct

from .config import settings


class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(settings.JWT_PRIVATE_KEY).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return Settings()


class NotVerified(Exception):
    pass


class UserNotFound(Exception):
    pass

class EmployeeNotFound(Exception):
    pass

class AdminNotFound(Exception):
    pass



async def require_user(Authorize: AuthJWT = Depends()):
    try:
        client = cnct.client

        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = userEntity(await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))}))
        
        if not user:
            raise UserNotFound('User no longer exist')

        if not user["verified"]:
            raise NotVerified('You are not verified')

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        if error == 'NotVerified':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return user_id










async def require_admin(Authorize: AuthJWT = Depends()):
    try:
        client = cnct.client

        Authorize.jwt_required()
        admin_id = Authorize.get_jwt_subject()
        admin = adminEntity(await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))}))
        
        if not admin:
            raise AdminNotFound('Admin no longer exist')

        if not admin["verified"]:
            raise NotVerified('You are not verified')

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'AdminNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Admin no longer exist')
        if error == 'NotVerified':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return admin_id