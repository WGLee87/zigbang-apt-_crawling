## zigbang(apt)_crawling


## Python을 이용한 직방 아파트 매물 리스트 크롤링(Crawling)


## 사용 라이브러리
requests
pandas
numpy
geohash


## 프로그램 소개
1. 특정 동이름을 입력하면 해당 동의 아파트 매물 검색

2. 크롤링 해오는 것 : [itemId, type, exclusive_type,	rent,	buildingFloor,	itemImages,	....	groupedItemFloor	agreementAreaName	isNew	sales (총 34개)]

3. 필요한 데이터만 전처리할 필요 있음

4. 크롤링 결과 : 리스트 -> 딕셔너리 -> df -> (csv로 원할 시 저장할 수 있음)
