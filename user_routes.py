from fastapi import APIRouter
from hive_connection import get_hive_conn

router = APIRouter()


@router.get("/user/{uid}/top10")
def user_top10(uid: int):
    query = f"""
        SELECT Movie_Name_Clean, Rating
        FROM movies
        WHERE User_Id = {uid}
        ORDER BY Rating DESC
        LIMIT 10
    """
    conn = get_hive_conn()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return {"uid": uid, "top10": rows}


@router.get("/user/{uid}/most-genres")
def user_most_watched_genres(uid: int):
    query = f"""
        SELECT Genre, COUNT(*) AS cnt
        FROM movies
        WHERE User_Id = {uid}
        GROUP BY Genre
        ORDER BY cnt DESC
    """
    conn = get_hive_conn()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return {"uid": uid, "most_watched_genres": rows}


@router.get("/user/{uid}/total")
def user_total_movies(uid: int):
    query = f"""
        SELECT COUNT(*) 
        FROM movies
        WHERE User_Id = {uid}
    """
    conn = get_hive_conn()
    cur = conn.cursor()
    cur.execute(query)
    total = cur.fetchall()[0][0]
    return {"uid": uid, "total_movies": total}


@router.get("/user/{uid}/last20")
def user_last20(uid: int):
    query = f"""
        SELECT Movie_Name_Clean, Rating, Timestamp
        FROM movies
        WHERE User_Id = {uid}
        ORDER BY Timestamp DESC
        LIMIT 20
    """
    conn = get_hive_conn()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return {"uid": uid, "last20": rows}

