# danger-logger

네트워크 프로그래밍 프로젝트에 고통받는 자의 고뇌가 담긴 작은 코드 뭉치들.

원격에서 실행되고 있는 docker 컨테이너 서비스를 제어해주는 프로그램입니다.

`docker-compose.yaml`파일이 위치한 경로와 제어를 원하는 컨테이너 이름들을 입력해주고, 접속을 원하는 서버의 IP와 Port를 알맞게 입력해주면 뚝딱!

## 사건의 발단

1. 네트워크 프로그래밍 과목에서 HTTP Request/Response 기반으로 동작하는 프로젝트(다르게 말해서 Django로 만든 웹 프로젝트)를 제안서로 제출.

2. HTTP Request/Response, WebSocket을 쓰더라도, TCP/UDP 소켓을 직접적으로 사용하는 부분이 꼭 들어가야 한다는 교수님의 말씀에 시작된 고민.

3. `"아! 그러면 TCP 소켓을 써서 서버를 제어 해보자 ^_____^"`

## 느낀점

- 그동안 과제 때문에 C로 소켓을 짜왔으나, Python 특유의 간결함과 탁월한 문자열 처리 능력에 감탄.

> Life is too short, You need python

- docker에서 만든 `docker-py`가 굉장히 좋음.. 여기저기 쓸모가 있는 듯 함.
