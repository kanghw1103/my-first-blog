from django import forms # 폼을 작성하기 위하여
from .models import Post # 포스트 모델을 임포트

class PostForm(forms.ModelForm): # ModelForm을 상속받아서

    class Meta: # Meta 클래스를 폼 클래스 내부에 정의
        model = Post # 폼을 작성할 모델을 지정
        fields =  ('title', 'text',) # 양식에서 입력 필요한 항목만 지정