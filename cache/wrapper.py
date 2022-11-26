from functools import wraps

from cache.connection import RedisCache


def fetch_from_cache(cache_name: str, cache_config: dict):

	cache = RedisCache(cache_config['redis']) #Подлючились к Redis
	print('cache=', cache)
	ttl = cache_config['ttl']

	def wrapper_func(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			cached_value = cache.get_value(cache_name)#Извлекаем из кэша
			print('cashed_value=', cached_value)
			if cached_value:
				return cached_value #Возвращаем извлеченное из кэша
			response = f(*args, **kwargs)# Если в кэше ничего нет, запускаем select из БД
			print('response=', response)
			cache.set_value(cache_name, response, ttl=ttl)
			return response
		return wrapper
	return wrapper_func
