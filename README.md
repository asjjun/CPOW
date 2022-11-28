# CPOW
### 캡스톤 디자인

<p align="center">
<img width="500px" src="https://user-images.githubusercontent.com/29851772/204193128-3dabef53-47d2-474e-b7ac-9a62d4c4e55d.png">
<br>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-2C2255?style=flat-square&logo=Flask&logoColor=white"/>
<img src="https://img.shields.io/badge/BlockChain-121D33?style=flat-square&logo=Bitcoin-SV&logoColor=white"/>
<br>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#프로젝트-소개">프로젝트 소개</a>
      <ul>
        <li><a href="#환경-설정">환경 설정</a></li>
      </ul>
    </li>
    <li><a href="#소개">소개</a></li>
    <li><a href="#본문-소개">본문 소개</a></li>
    <li><a href="#성능-분석">성능 분석</a></li>
    <li><a href="#결론">결론</a></li>
    <li><a href="https://www.youtube.com/watch?v=EDSXQ_lxfdk">Youtube Link</a></li>
    <li><a href="http://sigin.or.kr/sub03/sub0304.php?category=2&view=detail&no=207">SWCC-2022 논문제출 링크 [효율적 에너지 소비를 위한 구분화된 경잭적 합의 알고리즘]</a></li>
  </ol>
</details>

<br>

### *아래 내용은 간략하게 정리해놓은것이며, 자세한 정보는 논문을 참고

<br>

## 프로젝트 소개
 > 블록체인은 미래의 4차산업혁명을 이끌 기술로 평가된다. 대표적인 합의 알고리즘인 PoW는 탈중앙화와 보안성 면에서 장점을 보이지만 에너지 소비량이 많다는 단점이 있다. 따라서 채굴 과정을 단계별로 나누어 채굴 참여자 수를 제한하는 CPoW(Competition Proof Of Work)를 제안한다. 

## 환경 설정
  #### cpow_project : 
     파이썬 인터프리터 설정 (conda와 같은 가상환경은 동작하지 않는다.)
     
     인터프리터에 따라 terminal에 "pipenv run python main.py -p 5001" 혹은 "python main.py -p 5001"과 같이 원하는 port와 함께 실행
     * 중요: 최소 8개의 terminal 창으로 동작해야 정상적으로 체인이 생성되어 오류가 발생하지 않는다.
     
     postman 등을 사용해서
     http://localhost:5001/nodes/register         /    body: { "nodes":["http://127.0.0.1:5002"] }
     http://localhost:5002/nodes/register         /    body: { "nodes":["http://127.0.0.1:5001"] }
     http://localhost:5003~5010/nodes/help_nodes  /    body: { "nodes":["http://127.0.0.1:5001"] }
     를 post형식으로 보낸다. 
     * body 부분은 json 형식
     * 여기서 5003~5010은 port 개수에 따라 유동적으로 변경 ex) terminal 창이 8개라면 5003부터 5008까지 
     
     위와 같이 하는 이유는 5001 노드와 5002 노드를 먼저 등록하고 
     5003~5010 까지는 이미 연결되어있는 노드 중 하나에게 본인이 등록하겠다는 요청을 하면 연결되어 있는 모든 노드에게 등록이 되는 방식이기 때문이다.
     
     각 노드는 브라우저에서 http://localhost:5001, http://localhost:5002 등으로 접속 할 수 있다. 
     Chain을 누르면 현재 체인을 볼 수 있는데 처음엔 genesis block 하나만 있다.
     Start Mining을 누르면 로딩중인 아이콘과 함께 새 창이 뜨면서 채굴이 시작된다. 

     1등노드가 정보공유를 원하지 않는상황을 동작하고싶다면 "# 악성 노드 : True" 라고 적어둔 주석을 찾아 bad_first 값을 True로 바꾼다.
     위의 상황은 유튜브 영상에 더 자세히 나와있고 "1등노드가 정보를 공유하지않으며 시스템을 마비시키려는 악성 노드 일 경우" 라는 상황을 만든것이다.
     임의로 만든 상황이기 때문에 처음 1번만 정보 공유를 하지 않는다.
     
  #### CPOWSim :
      파이썬 인터프리터를 설정 후 main에서 동작


## 소개
PoW 방식은 소위 "채굴" 이라고 하는 작업을 통해 이루어진다. 이 작업은 채굴자들에 의해 이루어지는데, 채굴량은 리워드와 비례한다. 따라서 많은 채굴자들이 리워드를 얻기 위해 상당한 양의 컴퓨팅 파워를 동원하여 채굴 작업을 하고 여기에 천문학적인 전기 에너지가 소모된다. 기존의 PoW가 이런 문제를 갖고 있기에, PoW의 단점을 보완한 CPoW(Competition Proof of Work, 경쟁 작업 증명 방식)을 제안한다.

<br>

## 본문 소개
CPOW의 동작은 크게 세 개의 Round로 이루어진다. 첫Round의 채굴연산에서 첫번째로 정답을 도출한 노드는 다른 노드를 통해 검증을 받게 된다. 일반적인 PoW는 검증을 마치고 바로 체인에 블록을 올리지만, CPoW에서는 1등 노드 하나만 뽑고 끝나는 것이 아니라 참여 노드의 일정 비율만큼의 정답자를 더 받는다. 기존 PoW는 각 노드마다 해시연산 시 이전 해시 이외에 nonce만 달랐지만 CPoW는 nonce와 본인의 IP를 추가하여 각각 푸는 문제를 다르게 설계하였다.

<br>

## 성능 분석
CPOW방식의 전력소비량 개선을 평가하기 위해 BlockSim-simulator에 CPOW 알고리즘을 적용시켰다.

2019년 기준 한 대의 시스템이 소모하는 전기에너지 소모량은 200wh~800wh라고 한다. 에너지 소모량이 해마다 증가하는 것을 반영하여 전력 소비량의 범위를 600wh ~ 1200wh로 가정한다. 전력 소비량이 최소일 때와 최대일 때를 계산하여 기준선을 점선으로 그렸고 800wh일때의 환경에서 전력 소비량을 계산했다. 

![image](https://user-images.githubusercontent.com/29851990/174718162-5d22fb5c-eb26-4e5b-b9b1-b74c46e7400d.png)

<br>

## 결론
우리는 PoW의 합의과정을 세 단계로 나눔으로써 PoW의 장점은 그대로 유지하되 에너지 소비량을 줄이는 CPoW를 제안했다. 기존의 PoW는 모든 노드가 채굴에 참여하여 엄청난 컴퓨팅 리소스를 사용하기 때문에 이에 천문학적인 에너지 소비가 동원된다. 또한 시간이 지나고 난이도가 높아짐에 따라서 하나의 코인을 얻는데 필요한 에너지는 더 커진다. 이에 CPoW는 채굴 과정을 단계별로 나누어 단계 마다 채굴에 참여하는 노드 수를 일정 비율로 제한시켜 에너지 소비를 줄이는 효과를 볼 수 있다. 
