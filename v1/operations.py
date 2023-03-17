from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.encoders import jsonable_encoder
from .schema import *
from decouple import config
from .database import cnct

import os, sys, json, re

from datetime import datetime
from bson import json_util
from bson import ObjectId

from .database import cnct

from . import schema, oauth2
from v1.serializers import userResponseEntity #, employeeResponseEntity

from .analyser_Transformers import analyze_comments

router = APIRouter()


@router.on_event("startup")
async def create_db_client(cnct=cnct):
    try:
        MONGO_URI = os.environ.get('MONGO_URI') #used to get key value from heroku 'Setting/Config Vars' or through cli of any system
        if MONGO_URI is None:
            MONGO_URI = config('MONGO_URI') # used to get key value from ".env" usinng decouple

        cnct = cnct.init_db(MONGO_URI)
        print("Successfully connected to the Mongo Atlas Asynchronous database with 'motor' driver")

    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)


@router.on_event("shutdown")
async def shutdown_db_client():
    pass


@router.post("/", tags=["Home"])
async def home():
    return {"status": "Welcome to zaboRRR :)"}







@router.post("/user/post/create", tags=["Post CRUD"])
async def create_post(post : PostBaseSchema, user_id: str = Depends(oauth2.require_user)):

    client = cnct.client

    userData = await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))})
    
    if userData is None:
        return {"status": "No such user exist!"}
    

    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)', post.content)
    for s in sentences:
        if s == ' ':
            sentences.remove(' ')

    # print(type(sentences))
    # print(sentences)

        
    sentiment_results, positive, negative, neutral = analyze_comments(sentences)
    count = 0
    results = []
    sentiment_total = {"Positive" : positive, "Negative" : negative, "Neutral" : neutral}
    results.append(sentiment_total)
        
    for sentence in sentences:
        result = {}
        result["sentence"] = sentence
        result["sentiment"] = sentiment_results[count]["label"]
        result["score"] = sentiment_results[count]["score"]
        results.append(result)
        # print(count)
        count+=1
    positive = results[0].get('Positive')
    negative = results[0].get('Negative')
    neutral = results[0].get('Neutral')
        
    each_sentence_info_list = []
    cnt = 0
    for result in results[1:]:
        if cnt == 8:
            break
        each_sentence_info_list.append(result)
        # print(result)
        cnt+=1
    if negative > positive or negative > neutral:
        return  {"message":"We are restricting this post since this post contains inappropiate or negative content", "each_sentence_info_list": each_sentence_info_list, "data": True, "positive" : positive, "negative" : negative, "neutral" : neutral}
    

    post.created_by = userData.get("email")
    post.role = userData.get("role")
    post.name = userData.get("name")
    post.created_at = datetime.utcnow()
    post.updated_at = post.created_at

    await client.alumNation_db.post_collection.insert_one(dict(post))
    return dict(post)



@router.post("/user/post/all", tags=["Post CRUD"])
async def all_post(user_id: str = Depends(oauth2.require_user)):

    client = cnct.client

    userData = await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))})
    # print(userData.get("email"))
    if userData is None:
        return {"status": "No such user exist!"}

    
    all_post = client.alumNation_db.post_collection.find({'created_by': userData.get("email")})
    all_post = await all_post.to_list(length=100)
    return {"status": "success", "posts": json.loads(json_util.dumps(all_post))}



@router.post("/user/post/update", tags=["Post CRUD"])
async def update_post(updated_data : PostUpdateSchema, user_id: str = Depends(oauth2.require_user)):

    client = cnct.client

    userData = await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))})
    # print(userData.get("email"))
    if userData is None:
        return {"status": "No such user exist!"}
    
    updated_data.created_by = userData.get("email")
    updated_data.role = userData.get("role")
    updated_data.updated_at = datetime.utcnow()
    await client.alumNation_db.post_collection.update_one({'created_by': userData.get("email")}, {'$set': dict(updated_data)})
    return dict(updated_data)


@router.post("/user/post/delete", tags=["Post CRUD"])
async def delete_post(user_id: str = Depends(oauth2.require_user)):

    client = cnct.client

    userData = await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))})
    # print(userData.get("email"))
    if userData is None:
        return {"status": "No such user exist!"}
    
    await client.alumNation_db.post_collection.delete_one({'created_by': userData.get("email")})
    return {"status": "success", "message": "Post is successfully deleted!"}













@router.post("/admin/post/create", tags=["Post CRUD"])
async def create_post(post : PostBaseSchema, admin_id: str = Depends(oauth2.require_admin)):

    client = cnct.client

    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    # print(userData.get("email"))
    if adminData is None:
        return {"status": "No such admin exist!"}
    

    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)', post.content)
    for s in sentences:
        if s == ' ':
            sentences.remove(' ')

        
    sentiment_results, positive, negative, neutral = analyze_comments(sentences)
    count = 0
    results = []
    sentiment_total = {"Positive" : positive, "Negative" : negative, "Neutral" : neutral}
    results.append(sentiment_total)
        
    for sentence in sentences:
        result = {}
        result["sentence"] = sentence
        result["sentiment"] = sentiment_results[count]["label"]
        result["score"] = sentiment_results[count]["score"]
        results.append(result)
        # print(count)
        count+=1
    positive = results[0].get('Positive')
    negative = results[0].get('Negative')
    neutral = results[0].get('Neutral')
        
    each_sentence_info_list = []
    cnt = 0
    for result in results[1:]:
        if cnt == 8:
            break
        each_sentence_info_list.append(result)
        # print(result)
        cnt+=1
    if negative > positive or negative > neutral:
        return  {"message":"We are restricting this post since this post contains inappropiate or negative content", "each_sentence_info_list": each_sentence_info_list, "data": True, "positive" : positive, "negative" : negative, "neutral" : neutral}
    

    post.created_by = adminData.get("email")
    post.role = adminData.get("role")
    post.name = adminData.get("name")
    post.created_at = datetime.utcnow()
    post.updated_at = post.created_at

    await client.alumNation_db.post_collection.insert_one(dict(post))
    return dict(post)



@router.post("/admin/post/all", tags=["Post CRUD"])
async def all_post(admin_id: str = Depends(oauth2.require_admin)):

    client = cnct.client

    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    # print(adminData.get("email"))
    if adminData is None:
        return {"status": "No such admin exist!"}

    
    all_post = client.alumNation_db.post_collection.find({'created_by': adminData.get("email")})
    all_post = await all_post.to_list(length=100)
    return {"status": "success", "posts": json.loads(json_util.dumps(all_post))}



@router.post("/admin/post/update", tags=["Post CRUD"])
async def update_post(updated_data : PostUpdateSchema, admin_id: str = Depends(oauth2.require_admin)):

    client = cnct.client

    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    # print(adminData.get("email"))
    if adminData is None:
        return {"status": "No such admin exist!"}
    
    updated_data.created_by = adminData.get("email")
    updated_data.role = adminData.get("role")
    updated_data.updated_at = datetime.utcnow()
    await client.alumNation_db.post_collection.update_one({'created_by': adminData.get("email")}, {'$set': dict(updated_data)})
    return dict(updated_data)


@router.post("/admin/post/delete", tags=["Post CRUD"])
async def delete_post(admin_id: str = Depends(oauth2.require_admin)):

    client = cnct.client

    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    # print(adminData.get("email"))
    if adminData is None:
        return {"status": "No such admin exist!"}
    
    await client.alumNation_db.admin_collection.delete_one({'created_by': adminData.get("email")})
    return {"status": "success", "message": "Post is successfully deleted!"}







@router.post('/user/newsfeed', tags=["News Feed"])
async def newsfeed(user_id: str = Depends(oauth2.require_user)):
    client = cnct.client
    
    userData = await client.alumNation_db.user_collection.find_one({'_id': ObjectId(str(user_id))})
    if userData is None:
        return {"status": "No such user exist!"}

    all_post = client.alumNation_db.post_collection.find({})
    all_post = await all_post.to_list(length=100)
    return {"status": "success", "posts": json.loads(json_util.dumps(all_post))}


@router.post('/admin/newsfeed', tags=["News Feed"])
async def newsfeed(admin_id: str = Depends(oauth2.require_admin)):
    client = cnct.client
    
    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    if adminData is None:
        return {"status": "No such admin exist!"}

    all_post = client.alumNation_db.post_collection.find({})
    all_post = await all_post.to_list(length=100)
    return {"status": "success", "posts": json.loads(json_util.dumps(all_post))}









@router.post('/admin/dashboard/users/list/all', tags=["Admin Dashboard"])
async def newsfeed(admin_id: str = Depends(oauth2.require_admin)):
    client = cnct.client
    
    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    if adminData is None:
        return {"status": "No such admin exist!"}

    all_post = client.alumNation_db.user_collection.find({})
    all_post = await all_post.to_list(length=100)
    return {"status": "success", "posts": json.loads(json_util.dumps(all_post))}

@router.post('/admin/dashboard/users/list/alumni', tags=["Admin Dashboard"])
async def newsfeed(admin_id: str = Depends(oauth2.require_admin)):
    client = cnct.client
    
    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    if adminData is None:
        return {"status": "No such admin exist!"}

    all_post = client.alumNation_db.user_collection.find({'isAlumni': True})
    all_post = await all_post.to_list(length=100)
    return {"status": "success", "posts": json.loads(json_util.dumps(all_post))}

@router.post('/admin/dashboard/users/list/present_student', tags=["Admin Dashboard"])
async def newsfeed(admin_id: str = Depends(oauth2.require_admin)):
    client = cnct.client
    
    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    if adminData is None:
        return {"status": "No such admin exist!"}

    all_post = client.alumNation_db.user_collection.find({'isAlumni': False})
    all_post = await all_post.to_list(length=100)
    return {"status": "success", "posts": json.loads(json_util.dumps(all_post))}


@router.post('/admin/dashboard/users/count/all', tags=["Admin Dashboard"])
async def newsfeed(admin_id: str = Depends(oauth2.require_admin)):
    client = cnct.client
    
    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    if adminData is None:
        return {"status": "No such admin exist!"}

    total_users = await client.alumNation_db.user_collection.count_documents({})
    return {"status": "success", "total_users": total_users}


@router.post('/admin/dashboard/users/count/alumni', tags=["Admin Dashboard"])
async def newsfeed(admin_id: str = Depends(oauth2.require_admin)):
    client = cnct.client
    
    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    if adminData is None:
        return {"status": "No such admin exist!"}

    total_alumni = await client.alumNation_db.user_collection.count_documents({'isAlumni': True})
    return {"status": "success", "total_alumni": total_alumni}


@router.post('/admin/dashboard/users/count/present_student', tags=["Admin Dashboard"])
async def newsfeed(admin_id: str = Depends(oauth2.require_admin)):
    client = cnct.client
    
    adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
    if adminData is None:
        return {"status": "No such admin exist!"}

    total_present_student = await client.alumNation_db.user_collection.count_documents({'isAlumni': False})
    return {"status": "success", "total_present_student": total_present_student}








