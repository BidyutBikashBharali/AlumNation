from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from bson import json_util
from v1.serializers import userResponseEntity, adminResponseEntity #,  employeeResponseEntity, adminResponseEntity
import os, sys, json
from datetime import datetime

from .database import cnct

from . import schema, oauth2, utils

router = APIRouter()





@router.get("/user/profile/")
async def user_profile(user_id: str = Depends(oauth2.require_user)):
    try:
        client = cnct.client
        user = userResponseEntity(await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))}))

        return {"status": "success", "result": user}

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line  ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)





@router.get("/user/profile/{user_id}")
async def user_profile_by_id(user_id: str):
    try:
        client = cnct.client
        user = userResponseEntity(await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))}))
        scrap_req = await client.alumNation_db.alumNation_collection.find_one({'ph_no': user["ph_no"]})
        data = []
        data.append(user)
        data.append(scrap_req)
        result = json.loads(json_util.dumps(data))
        return {"status": "success", "result": result}

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line  ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)





@router.post("/user/profile/update")
async def user_profile_update(updated_data : schema.UserUpdateSchema, user_id: str = Depends(oauth2.require_user)):
    try:
        client = cnct.client
        userData = await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))})

        if userData is None:
            return {"status": "No such user exist!"}
        
        isEmailExist = await client.alumNation_db.user_collection.find_one({'email': updated_data.email})

        if isEmailExist is None and userData.get("email") != updated_data.email:
            return {"status": "Username is already exist. Try with a different email address!"}
        

        if len(updated_data.password) == 0 or len(updated_data.passwordConfirm) == 0:
            updated_data.password = userData.get("password")
        if len(updated_data.password) >=8 or len(updated_data.passwordConfirm) >= 8:
            if updated_data.password == updated_data.passwordConfirm:
                updated_data.password = utils.hash_password(updated_data.password)
                del updated_data.passwordConfirm
            else:
                return {"message": "'password' and 'passwordConfirm' field is not matching!"}
            
        updated_data.address = dict(updated_data.address)
        updated_data.others = dict(updated_data.others)
        updated_data.updated_at = datetime.utcnow()
        await client.alumNation_db.user_collection.update_one({'_id': ObjectId(str(user_id))}, {'$set': dict(updated_data)})
        userData = await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))})
        user = userResponseEntity(userData)
        
        # scrap_req = await client.alumNation_db.alumNation_collection.find_one({'ph_no': user["ph_no"]})
        # data = []
        # data.append(user)
        # data.append(scrap_req)
        # result = json.loads(json_util.dumps(data))
        return {"status": "success", "result": user}

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line  ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)




@router.get("/user/profile/delete")
async def user_profile_delete(user_id: str = Depends(oauth2.require_user)):
    try:
        client = cnct.client
        userData = await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))})
        # print(userData)
        if userData is None:
            return {"status": "No such user exist!"}
        await client.alumNation_db.user_collection.delete_one({'_id': ObjectId(str(user_id))})
        return {"status": "success", "message": "User is successfully deleted!"}

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line  ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
























@router.get("/admin/profile/")
async def admin_profile(admin_id: str = Depends(oauth2.require_admin)):
    try:
        client = cnct.client
        admin = adminResponseEntity(await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))}))
        return {"status": "success", "result": admin}

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line  ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)




@router.get("/admin/profile/{admin_id}")
async def admin_profile(admin_id: str):
    try:
        client = cnct.client
        admin = adminResponseEntity(await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))}))
        return {"status": "success", "result": admin}

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line  ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)





@router.post("/admin/profile/update")
async def admin_profile_update(updated_data : schema.AdminUpdateSchema, admin_id: str = Depends(oauth2.require_admin)):
    try:
        client = cnct.client
        adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
        
        if adminData is None:
            return {"status": "No such admin exist!"}
        
        isEmailExist = await client.alumNation_db.admin_collection.find_one({'email': updated_data.email})
        
        if isEmailExist is None and adminData.get("email") != updated_data.email:
            return {"status": "Username is already exist. Try with a different email address!"}

        if len(updated_data.password) == 0 or len(updated_data.passwordConfirm) == 0:
            updated_data.password = adminData.get("password")
        if len(updated_data.password) >=8 or len(updated_data.passwordConfirm) >= 8:
            if updated_data.password == updated_data.passwordConfirm:
                updated_data.password = utils.hash_password(updated_data.password)
                del updated_data.passwordConfirm
            else:
                return {"message": "'password' and 'passwordConfirm' field is not matching!"}

        updated_data.address = dict(updated_data.address)
        updated_data.others = dict(updated_data.others)
        updated_data.updated_at = datetime.utcnow()
        await client.alumNation_db.admin_collection.update_one({'_id': ObjectId(str(admin_id))}, {'$set': dict(updated_data)})
        adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
        admin = adminResponseEntity(adminData)

        return {"status": "success", "result": admin}

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line  ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)




@router.get("/admin/profile/delete")
async def admin_profile_delete(admin_id: str = Depends(oauth2.require_admin)):
    try:
        client = cnct.client
        adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
        # print(adminData)
        if adminData is None:
            return {"status": "No such admin exist!"}
        await client.alumNation_db.admin_collection.delete_one({'_id': ObjectId(str(admin_id))})
        return {"status": "success", "message": "Admin is successfully deleted!"}

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line  ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)

