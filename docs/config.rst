Config
======

gaia_conf.json
--------------

``./gaia_conf.json`` 파일은 S3 Bucket Path를 저장하는데 사용됩니다.
json 형태의 key, value 값을 통해서 관리되는데 저장되는 값은 bucket name과 folder의 경로들이 저장됩니다.

gaia_conf.json파일은

.. literalinclude:: ../gaia_conf.json.example
     :language: json

처럼 사용합니다.

Bucket Name은 gaia에서 key값으로 이용되므로 실제 S3에 생성되어있는 Bucket Name과 같아야합니다. 하지만 folder의 경우 key에 대응되는 value가 이용되기 때문에 키의 명명은 자유롭습니다. 또한 gaia는 S3 Bucket Path가 날짜 단위로
나뉘어져 있는 경우에도 문제 없이 대응합니다. 예를 들어 실제 경로가 ``log/path/<년>/<월>/<일>/`` 로 날짜마다 가변적으로 대응되어야 한다면 위의 예시와 같이 ``<>`` 를 사용하여 대응할 수 있습니다.