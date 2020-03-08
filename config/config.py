# mysql配置
DATABASE_URI = 'mysql+pymysql://jiangshipan:19980502@119.3.212.165:3306/intel_logistics?charset=utf8mb4'

# redis配置
REDIS_HOST = '119.3.212.165'
REDIS_PORT = '6379'


# 按距离基础费用, 单位km
DISTANCE_COST = {
    10: 10,
    20: 20,
    30: 30,
    40: 40,
    50: 50,
    60: 60,
    70: 70,
    80: 80,
    90: 90
}
