def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "ph_no": user["ph_no"],
        "role": user["role"],
        # "address": user["address"],
        # "others": user["others"],
        "address": user["address"],
        "about_me": user["about_me"],
        "fb": user["fb"],
        "insta": user["insta"],
        "git": user["git"],
        "linked": user["linked"],
        # "photo": user["photo"],
        "verified": user["verified"],
        "password": user["password"],
        "branch": user["branch"],
        "institute": user["institute"],
        "passout_year": user["passout_year"],
        "isAlumni": user["isAlumni"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def userResponseEntity(user) -> dict:
    # print("@@@@@@@@@@@@@" , user)
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "ph_no": user["ph_no"],
        "role": user["role"],
        "address": user["address"],
        "about_me": user["about_me"],
        "fb": user["fb"],
        "insta": user["insta"],
        "git": user["git"],
        "linked": user["linked"],
        # "photo": user["photo"],
        "branch": user["branch"],
        "institute": user["institute"],
        "passout_year": user["passout_year"],
        "isAlumni": user["isAlumni"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }






def adminEntity(admin) -> dict:
    return {
        "id": str(admin["_id"]),
        "name": admin["name"],
        "email": admin["email"],
        "ph_no": admin["ph_no"],
        "role": admin["role"],

        "address": admin["address"],
        "about_me": admin["about_me"],
        "fb": admin["fb"],
        "insta": admin["insta"],
        "git": admin["git"],
        "linked": admin["linked"],
        # "photo": admin["photo"],
        "verified": admin["verified"],
        "password": admin["password"],
        "branch": admin["branch"],
        "institute": admin["institute"],
        "passout_year": admin["passout_year"],
        "isAlumni": admin["isAlumni"],
        "created_at": admin["created_at"],
        "updated_at": admin["updated_at"]
    }


def adminResponseEntity(admin) -> dict:
    return {
        "id": str(admin["_id"]),
        "name": admin["name"],
        "email": admin["email"],
        "ph_no": admin["ph_no"],
        "role": admin["role"],

        # "photo": admin["photo"],
        "address": admin["address"],
        "about_me": admin["about_me"],
        "fb": admin["fb"],
        "insta": admin["insta"],
        "git": admin["git"],
        "linked": admin["linked"],
        "branch": admin["branch"],
        "institute": admin["institute"],
        "passout_year": admin["passout_year"],
        "isAlumni": admin["isAlumni"],
        "created_at": admin["created_at"],
        "updated_at": admin["updated_at"]
    }


