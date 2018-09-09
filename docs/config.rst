Config
======

``gaia_conf.json``
------------------

``./gaia_conf.json`` 파일은 S3 Bucket Path를 저장하는데 사용됩니다.
json 형태의 key, value 값을 통해서 key는 bucket name을, value는 bucket name을 제외한 S3 경로를 입력합니다.

gaia_conf.json파일은

.. literalinclude:: ../gaia_conf.json.example
     :language: json

처럼 사용합니다.

Bucket Name은 gaia에서 key값으로 이용되므로 실제 S3에 생성되어있는 Bucket Name과 같아야합니다.