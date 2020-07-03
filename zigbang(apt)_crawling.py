#!/usr/bin/env python
# coding: utf-8

# ### 직방
# - 동이름을 입력하면 아파트 매물을 데이터 프레임으로 만들기
# - robots.txt

# #### 1. 웹서비스 분석 : URL 찾기, 크롤링 전략 세우기
# 
# - 동이름 입력 -> lat, lng
# - lat, lng -> geohash : geohash 패키지 설치
# - geohash -> item ids
# - item ids -> item datas(데이터 프레임)

# #### 함수로 만들기
# - 동이름 -> 아파트 매물 데이터 프레임

# In[ ]:


import requests
import numpy
import pandas as pd
import geohash2


# In[39]:


def crawling_apt(addr):
    # 동이름 -> 위도,경도
    url = "https://apis.zigbang.com/search?q={}".format(addr)
    response = requests.get(url)
    data = response.json()["items"][0]
    lat, lng = data["lat"], data["lng"]
    
    # 위도,경도 -> geohash
    geohash = geohash2.encode(lat, lng, precision=5)
    
    # geohash -> ids
    url = "https://apis.zigbang.com/property/apartments/items?domain=zigbang&geohash={}&q=type=sales%7Cprice=0~-1%7CfloorArea=0~-1".format(geohash)
    response = requests.get(url)
    datas = response.json()["items"]
    ids = [data["itemId"] for data in datas]
    
    # ids -> items : 200개씩
    dfs = []
    for idx in range(0, len(ids), 200):
        start, end = idx, idx+200
        ids_str = str(ids[start:end]).replace(" ", "")
        url = "https://apis.zigbang.com/property/apartments/items?        vritemIds={ids}&itemIds={ids}&citemIds={ids}".format(ids=ids_str)
        response = requests.get(url)
        datas = response.json()["items"]
        item_df = pd.DataFrame(datas)
        columns = [ "itemId", 'apartmentName',"buildingFloor", "groupedItemFloor", "grossArea", "lat", "lng", "sales", "itemTitle" ]
        item_df = item_df[columns]
        item_df["m2"] = item_df["grossArea"].apply(lambda data: data["m2"])
        item_df["p"] = item_df["grossArea"].apply(lambda data: data["p"])
        item_df.drop(columns=["grossArea"], inplace=True)
        dfs.append(item_df)
    result_df = pd.concat(dfs)
    result_df.reset_index(drop=True, inplace=True)
    
    return result_df

