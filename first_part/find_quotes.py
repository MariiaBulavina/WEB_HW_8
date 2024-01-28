from typing import Any
from pprint import pprint

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:

    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:

    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def main():

    while True:

        user_input = input('Enter the command. To finish enter "exit": ')

        if user_input == 'exit':
            break

        user_input = user_input.split(':')
        command = user_input[0]
        data = user_input[1].strip()

        match command:

            case 'name':

                result = find_by_author(data)
                pprint(result)

            case 'tag':

                result = find_by_tag(data)
                pprint(result)

            case 'tags':

                result = []
                
                data = data.split(',')
                for teg in data:
                    r = find_by_tag(teg)
                    if r not in result:
                        result.append(r)

                pprint(result)
    
 
if __name__ == '__main__':

    main()
