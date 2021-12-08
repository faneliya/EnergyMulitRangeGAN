


sqlTextWindBelgium3M = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "

sqlTextWindBelgium6M = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "


sqlTextWindBelgium1Y = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "


sqlTextWindBelgium2Y = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "


sqlTextWindBelgium5Y = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "


sqlTextWindBelgiumAll = "SELECT	SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "

sqlTextSolarBelgium = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	SOLAR_PW AS PW," \
          "	SOLAR_PW_CAPA AS CAPA," \
          "	TEMP_MAX " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "


sqlTextSolarBelgiumAll = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	SOLAR_PW AS PW," \
          "	SOLAR_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "


sqlTextBelgiumEnergyAll = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	SOLAR_PW + WIND_PW AS PW," \
          "	SOLAR_PW_CAPA + WIND_PW_CAPA AS CAPA," \
          "	SOLAR_PW AS SOLAR_PW," \
          "	SOLAR_PW_CAPA AS SOLAR_CAPA," \
          "	WIND_PW AS WIND_PW," \
          "	WIND_PW_CAPA AS WIND_CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190101' AND '20210401' "


sqlTextWindBelgiumAllM3 = "SELECT	SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20210101' AND '20210401' "


sqlTextWindBelgiumAllM6 = "SELECT	SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20201001' AND '20210401' "


sqlTextWindBelgiumAllY1 = "SELECT	SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20200401' AND '20210401' "


sqlTextWindBelgiumAllY2 = "SELECT	SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20190401' AND '20210401' "


sqlTextWindBelgiumAllY5 = "SELECT	SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20160401' AND '20210401' "

