![image](/resource/speechteacher_logo.jpg){width="90%"}

## ✨사용자 음성 분석을 통한 맞춤형 발표 코칭 서비스✨  


## ✨Soma_MainServer✨  
- [Soma_MainServer](https://git.swmgit.org/swm-12/12_swm48/soma_mainserver){:target="_blank"}
- [Soma_IOS](https://git.swmgit.org/swm-12/12_swm48/soma_ios){:target="_blank"}
- [Soma_ML](https://git.swmgit.org/swm-12/12_swm48/soma_ml){:target="_blank"}
<br>

## 개요  
- 머신러닝 분석을 통한 음성 및 어휘적 측면에 특화된 발표 연습 피드백 서비스제공
- 사용자에게 발표 연습을 위한 다양한 UI/UX 환경 제공 
- 시/공간적 제약을 줄여주는 모바일 앱 서비스 제공

## 시스템 구성도  
![image](/resource/system_structure.PNG){.width="90%}

## AWS 구성도  
![image](/resource/AWS_structure.png){.width="90%}

## ERD
![image](/resource/ERD_structure.png){.width="90%}


## 회원관리 API

- view.py 
로그인, 비밀번호찾기, 회원가입, 정보조회, 정보수정, 회원탈퇴 등 API구현<br>
- models.py
자료를 DB에 저장하기 위한 ST_USER 테이블 ORM구현<br>
- utils.py
로그인이 필요한 기능을 사용할때 체크해주는 login_check함수 구현<br>
-serializers.py
직렬화를 통해 DB쿼리 결과를 쉽게 json형식으로 변경<br>