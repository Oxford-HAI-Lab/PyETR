# # import math
# import json
# import marshal
# import types
# import base64
# from pydantic import BaseModel

# def log(x: float) -> float:
#     import math

#     return math.log(x, 10)


# def serialize_function(func):
#     if not callable(func):
#         raise ValueError("Input must be a callable function")

#     code = func.__code__
#     serialized_function = {
#         "code": base64.b64encode(marshal.dumps(code)).decode("utf-8"),
#         "name": func.__name__,
#     }
#     return json.dumps(serialized_function)


# def deserialize_function(serialized_function):
#     deserialized_function_data = json.loads(serialized_function)
#     bytecode = base64.b64decode(deserialized_function_data["code"].encode("utf-8"))
#     code = marshal.loads(bytecode)
#     return types.FunctionType(code, globals(), deserialized_function_data["name"])


# new_serial = '{"code": "4wEAAAAAAAAAAAAAAAQAAAADAAAA8zYAAACXAGQBZABsAH0BfAGgAQAAAAAAAAAAAAAAAAAAAAAAAAAAfABkAqYCAACrAgAAAAAAAAAAUwCpA07pAAAAAOkKAAAAqQLaBG1hdGjaA2xvZ6kC2gF4cgYAAABzAgAAACAg+i8vaG9tZS9tYXJrLXRvZGQvUHlFVFIvcHlldHIvZGF0YV9wYXJzZXIvdGVzdC5wedoQZXhhbXBsZV9mdW5jdGlvbnILAAAALQAAAPMdAAAAgADYBA+AS4BLgEvYCw+POIo4kEGQcok/jD/QBBrzAAAAAA==", "name": "example_function"}'

# deserialized_example = deserialize_function(new_serial)
# print(deserialized_example)
# result = deserialized_example(3)
# print("Deserialized Function Result:", result)
