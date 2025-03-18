from typing import Union, Dict, List, Literal, Optional, TypedDict

class ResizeOptions(TypedDict,total=False):
    method: Literal['scale', 'fit', 'cover', 'thumb']
    width: Optional[int]
    height: Optional[int]

ConvertTypes = Literal['image/webp', 'image/jpeg', 'image/png', "image/avif", "*/*"]
class ConvertOptions(TypedDict, total=False):
    type: Union[ConvertTypes, List[ConvertTypes]]

class TransformOptions(TypedDict, total=False):
    background: Union[str, Literal["white", "black"]]

class S3StoreOptions(TypedDict, total=False):
    service: Literal['s3']
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str
    path: str
    headers: Optional[Dict[str, str]]
    acl: Optional[Literal["no-acl"]]

class GCSStoreOptions(TypedDict, total=False):
    service: Literal['gcs']
    gcp_access_token: str
    path: str
    headers: Optional[Dict[str, str]]

PreserveOption = Literal['copyright', 'creation', 'location']
