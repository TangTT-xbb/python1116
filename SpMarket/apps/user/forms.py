import re

from django import forms

from user.helper import set_password
from user.models import SpUser, UserAddress
from django_redis import get_redis_connection


class RegisterModelForm(forms.ModelForm):
    """注册表单，验证"""
    # 单独添加字段
    password = forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required': "密码必填",
                                   'max_length': "密码长度不能大于16个字符",
                                   'min_length': "密码长度不能小于6个字符",
                               }
                               )

    re_password = forms.CharField(error_messages={'required': "密码必填"})

    verify_code = forms.CharField(error_messages={'required': "验证码必填",
                                                  r'^[0-9]\d{5}$': '请填写正确的手机号码'})

    agree = forms.BooleanField(required=True, error_messages={'required': "请同意用户协议"})

    class Meta:
        model = SpUser
        # 需要验证的字段
        fields = ['phone', ]
        error_messages = {
            "phone": {'required': "手机号码必填"}
        }

    def clean_phone(self):
        # 验证手机号码是否唯一
        phone = self.cleaned_data.get('phone')
        rs = SpUser.objects.filter(phone=phone).exists()  # 返回bool
        if rs:
            raise forms.ValidationError("手机号码已经被注册")
        else:
            return phone

    # 单独清洗
    def clean(self):
        # 验证两个密码是否一样
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('re_password')
        if pwd1 and pwd2 and pwd1 != pwd2:
            # 确认密码错误
            raise forms.ValidationError({"re_password": "两次密码输入不一致"})
        # 这个号码必须和发送给用户的号码一致 ？？？？

        try:
            verify_code = self.cleaned_data.get('verify_code', "")
            phone = self.cleaned_data.get('phone', 'phone')
            r = get_redis_connection()
            re_verify_code = r.get(phone)
            re_verify_code = re_verify_code.decode('utf-8')  # 把二进制转换为str
            if verify_code and verify_code != str(re_verify_code):
                raise forms.ValidationError({"verify_code": "验证码输入错误"})
        except:
            raise forms.ValidationError({"verify_code": "验证码输入错误"})

        """or ( 注释部分暂未发现bug)
                verify_code = self.cleaned_data.get('verify_code', "")
                phone = self.cleaned_data.get('phone', 'phone')
                r = get_redis_connection()
                re_verify_code = r.get(phone)
                re_verify_code = re_verify_code.decode('utf-8')  # 把二进制转换为str
                if verify_code and verify_code != str(re_verify_code):
                    raise forms.ValidationError({"verify_code": "验证码输入错误"})"""

        return self.cleaned_data


class LoginModelForm(forms.ModelForm):
    # 登录表单 验证

    # verify_code = forms.CharField(error_messages={'required': "验证码必填"})

    class Meta:
        model = SpUser
        # 需要验证的字段
        fields = ['phone', 'password']
        error_messages = {
            "phone": {'required': "请填写手机号码"},
            "password": {'required': "请填写密码"}
        }

    def clean(self):
        # 验证手机号和密码
        # 获取手机号和密码
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        # 验证
        try:
            user = SpUser.objects.get(phone=phone)
        except SpUser.DoesNotExist:
            raise forms.ValidationError({"phone": '该手机号码未注册'})
        # 验证密码
        if user.password != set_password(password):
            # 确认密码错误
            raise forms.ValidationError({"password": "密码输入错误!"})

        # 将用户信息保存到cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data


class ForgetpwdModelForm(forms.ModelForm):
    password = forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required': "密码必填",
                                   'max_length': "密码长度不能大于16个字符",
                                   'min_length': "密码长度不能小于6个字符",
                               }
                               )

    re_password = forms.CharField(error_messages={'required': "密码必填"})

    class Meta:
        model = SpUser
        # 需要验证的字段
        fields = ['phone', ]
        error_messages = {
            "phone": {'required': "请填写手机号码"},
        }

    # 单独清洗
    def clean(self):
        # 验证两个密码是否一样
        phone = self.cleaned_data.get('phone')
        if re.match(r'^1[3-9]\d{9}$', str(phone)):
            try:
                phone == SpUser.objects.filter(phone=phone)
            except SpUser.DoesNotExist:
                raise forms.ValidationError({"phone": '手机号码填写错误'})

        else:
            raise forms.ValidationError({"phone": "手机号码非法"})
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('re_password')
        if pwd1 and pwd2 and pwd1 != pwd2:
            # 确认密码错误
            raise forms.ValidationError({"re_password": "两次密码输入不一致"})
        return self.cleaned_data


class UpdatepwdModelForm(forms.ModelForm):
    old_password = forms.CharField(error_messages={'required': "原密码必填"})
    password = forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required': "新密码必填",
                                   'max_length': "密码长度不能大于16个字符",
                                   'min_length': "密码长度不能小于6个字符",
                               }
                               )
    re_password = forms.CharField(error_messages={'required': "确认密码必填"})

    class Meta:
        model = SpUser
        # 需要验证的字段
        fields = ['password', ]
        error_messages = {
            "password": {'required': "请填写密码"},
        }

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        old_password = set_password(old_password)
        try:
            old_password == SpUser.objects.filter(password=old_password)
        except SpUser.DoesNotExist:
            raise forms.ValidationError({"old_password": '密码输入错误'})
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('re_password')
        if pwd1 and pwd2 and pwd1 != pwd2:
            # 确认密码错误
            raise forms.ValidationError({"re_password": "两次密码输入不一致"})

        return self.cleaned_data


class AddressModelForm(forms.ModelForm):
    """用户添加收货地址的表单"""

    class Meta:
        model = UserAddress
        exclude = ['create_time', 'update_time', 'is_delete', 'user']
        error_messages = {
            'username': {
                'required': "请填写用户名！",
            },
            'phone': {
                'required': "请填写手机号码！",
            },
            'brief': {
                'required': "请填写详细地址！",
            },
            'hcity': {
                'required': "请填写完整地址！",
            },
        }

    def clean(self):
        # 验证如果数据库里地址已经超过6条报错
        cleaned_data = super().clean()
        count = UserAddress.objects.filter(user_id=self.data.get("user_id")).count()
        if count >= 6:
            raise forms.ValidationError({"hcity": "收货地址最多只能保存6条"})

            # 操作默认值
            # 如果当前是默认地址,其他 就设置为False
        if cleaned_data.get('isDefault'):
            UserAddress.objects.filter(user_id=self.data.get("user_id")).update(isDefault=False)
        return cleaned_data
