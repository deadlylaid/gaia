Command
=======

gen
---
gen 명령어는 2가지 역할을 합니다.

* 첫째로,  ``gaia_conf.json`` 이 존재하지 않을 경우 이를 생성합니다.
* 둘째로, bucket name과 path 값을 추가할 수 있습니다.

물론 gen 명령어는 둘 중의 한가지 기능만 필요할 경우에도 지원합니다. 전자의 경우 argument를 입력하지 않아도 됩니다.

find
----

``gaia_conf.json`` 파일에서 지정된 설정 값을 이용해서 로그를 검색하는 명령어 입니다.
bucket name과 keyword를 변수로 받고 명령어를 실행합니다.

keyword에 매치되는 로그가 있다면 해당 로그를 반환하지만 없다면 ``keyword does not exist`` 를 반환합니다.