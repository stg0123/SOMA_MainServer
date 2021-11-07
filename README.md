<center><img src="/resource/speechteacher_logo.png" width="90%"/></center>

## ✨사용자 음성 분석을 통한 맞춤형 발표 코칭 서비스✨  


## ✨Soma_MainServer✨  
- [Soma_MainServer](https://git.swmgit.org/swm-12/12_swm48/soma_mainserver)
- [Soma_IOS](https://git.swmgit.org/swm-12/12_swm48/soma_ios)
- [Soma_ML](https://git.swmgit.org/swm-12/12_swm48/soma_ml)
<br>

## 개요  
- 머신러닝 분석을 통한 음성 및 어휘적 측면에 특화된 발표 연습 피드백 서비스제공
- 사용자에게 발표 연습을 위한 다양한 UI/UX 환경 제공 
- 시/공간적 제약을 줄여주는 모바일 앱 서비스 제공

## 팀 소개
팀명 : 말선생<br>
팀원 : 손태균 ,손승열<br>


## 🌟시스템 구성도  
![image](/resource/system_structure.png)

## 🔎AWS 구성도  
![image](/resource/aws_structure.png)

## ⚙️ERD
![image](/resource/ERD_structure.png)


## 😥회원관리 API

- view.py <br>
회원관리, 발표연습, 발표자료, 발표키워드, 발표대본, 발표결과 CRUD 수행 API 구현<br>

- models.py<br>
st_user, presentation, presentation_file, presentation_keyword, presentation_script, presentation_result, knowhow 테이블 대응 모델 생성<br>

- utils.py<br>
로그인이 필요한 기능을 사용할때 체크해주는 login_check함수 구현<br>

- serializers.py<br>
직렬화를 통해 DB쿼리 결과를 쉽게 json형식으로 변경<br>

