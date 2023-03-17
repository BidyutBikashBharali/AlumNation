from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException

from .import oauth2, schema

from .database import cnct

from .serializers import userEntity, userResponseEntity, adminResponseEntity, adminEntity # ,employeeEntity, employeeResponseEntity,
from . import schema, utils
from .oauth2 import AuthJWT
from .config import settings


router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN





@router.post('/user/register', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
async def create_user(payload: schema.CreateUserSchema):
    client = cnct.client

    
    user = await client.alumNation_db.user_collection.find_one({'email': payload.email.lower()})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    
    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    payload.role = 'user'
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = await client.alumNation_db.user_collection.insert_one(payload.dict())
    new_user = userResponseEntity(await client.alumNation_db.user_collection.find_one({'_id': result.inserted_id}))
    return {"status": "success", "user": new_user}



@router.post('/user/login')
async def login(payload: schema.LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()):
    client = cnct.client

    
    db_user = await client.alumNation_db.user_collection.find_one({'email': payload.email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    user = userEntity(db_user)

    
    if not utils.verify_password(payload.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    
    access_token = Authorize.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    
    refresh_token = Authorize.create_refresh_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    
    return {'status': 'success', 'access_token': access_token}



@router.get('/user/token/refresh')
async def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        client = cnct.client

        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = userEntity(await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))}))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}



@router.get('/user/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}

















@router.post('/admin/register', status_code=status.HTTP_201_CREATED, response_model=schema.AdminResponse)
async def create_admin(payload: schema.CreateAdminSchema):
    client = cnct.client

 
    admin = await client.alumNation_db.admin_collection.find_one({'email': payload.email.lower()})
    if admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    
    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')

    payload.password = utils.hash_password(payload.password)
    del payload.passwordConfirm
    payload.role = 'admin'
    payload.verified = True
    payload.email = payload.email.lower()
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    result = await client.alumNation_db.admin_collection.insert_one(payload.dict())
    new_admin = adminResponseEntity(await client.alumNation_db.admin_collection.find_one({'_id': result.inserted_id}))
    return {"status": "success", "admin": new_admin}



@router.post('/admin/login')
async def login(payload: schema.LoginAdminSchema, response: Response, Authorize: AuthJWT = Depends()):
    client = cnct.client

 
    db_admin = await client.alumNation_db.admin_collection.find_one({'email': payload.email.lower()})
    if not db_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    admin = adminEntity(db_admin)


    if not utils.verify_password(payload.password, admin['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    access_token = Authorize.create_access_token(
        subject=str(admin["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

 
    refresh_token = Authorize.create_refresh_token(
        subject=str(admin["id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')


    return {'status': 'success', 'access_token': access_token}



@router.get('/admin/token/refresh')
async def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        client = cnct.client

        Authorize.jwt_refresh_token_required()

        admin_id = Authorize.get_jwt_subject()
        if not admin_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        admin = adminEntity(await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))}))
        if not admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The admin belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(admin["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}



@router.get('/admin/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), admin_id: str = Depends(oauth2.require_admin)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}

