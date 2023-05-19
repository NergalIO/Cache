import typing, pathlib, json
import hashlib

def hash(*args, **kwargs):
    return hashlib.md5(json.dumps([*args, kwargs], sort_keys=True).encode("cp1251")).hexdigest()

class Cache:
    def __init__(self, file: typing.AnyStr = "cache.json") -> None:
        self.cache = {}
        self.file = pathlib.Path(file)
        
        if not self.file.exists():
            self.file.touch()
            with self.file.open('w') as file:
                file.write("{}")
        else:
            self.__load__()
    
    def Decorator(self, func: typing.Callable) -> typing.Any:
        def wrapper(*args, **kwargs) -> typing.Any:
            _hash = hash(*args, **kwargs)
            if _hash in self.cache:
                return self.cache[_hash]
            result = func(*args, **kwargs)
            self.cache[_hash] = result
            return result
        return wrapper
    
    def __load__(self) -> None:
        with self.file.open("r") as file:
            self.cache = json.loads(file.read())

    def __save__(self) -> None:
        prev_data = ""
        with self.file.open("r") as file:
            prev_data = file.read()
        
        with self.file.open("w") as file:
            decoded = json.loads(prev_data)
            file.write(json.dumps(decoded | self.cache, indent=2))
