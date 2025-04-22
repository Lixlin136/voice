import json
import uuid

from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import logging
from utils.nlp_processor import polish_results_with_llm

logging.basicConfig(level=logging.INFO)
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

# 登录视图
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, CustomUserCreationForm, SignatureForm, EmailForm, PhoneForm, NicknameForm, AvatarForm
from .models import CustomUser, VerificationCode
from django.utils import timezone
from datetime import timedelta


@csrf_exempt
def set_persona(request):
    print("request.POST", request.POST)
    if request.method == 'POST':
        # print("request.body", request.body.decode("utf-8"))
        # 必须解码
        # request.POST <QueryDict: {'csrfmiddlewaretoken': ['MdUGY0UCKCUyy8Y9TTbrjK8th8JGxgr7sox6MU8dW9uC3qwZyHKV0CqfkwPaoHTb'], 'persona_style': ['standard_female'], 'persona_name': ['ai萝莉']}>
        # request.body b'csrfmiddlewaretoken=MdUGY0UCKCUyy8Y9TTbrjK8th8JGxgr7sox6MU8dW9uC3qwZyHKV0CqfkwPaoHTb&persona_style=standard_female&persona_name=ai%E8%90%9D%E8%8E%89'
        #  显式解码为UTF-8字符串
        # data = json.loads(request.body.decode('utf-8'))
        request.session['persona_name'] = request.POST.get('persona_name')
        request.session['persona_style'] = request.POST.get('persona_style')
        request.session['persona_description'] = request.POST.get('persona_description')
        request.session['persona_voice'] = request.POST.get('persona_voice')
        # request.session['persona_language'] = request.POST.get('persona_language')
        print(request.session['persona_name'])
        print(request.session['persona_style'])
        # 清除聊天纪录
        request.session['conversation_history'] = []
        print(request.session['conversation_history'])
        request.session.modified = True
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# 注册视图
def register(request):
    print(request.POST)  # 调试输出
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form.is_valid())
        # print(form.error_messages)
        if form.is_valid():
            form.save()  # 保存用户信息
            username = form.cleaned_data.get('username')
            # messages.success(request, f'Account created for {username}!')
            return redirect('login')  # 注册成功后跳转到登录页面
    else:
        form = UserCreationForm()  # 初始化空表单（GET请求时）
    return render(request, 'register.html', context={'form': form})


def send_verification_code(request):
    if request.method == 'POST':
        try:
            if isinstance(request.user, AnonymousUser):
                email = request.POST.get('email')
                print("email", email)
                user = CustomUser.objects.get(email=email)
            else:
                user = request.user
                email = user.email
            print('send_verification_code_user', user)
            code = user.generate_verification_code()
            print("code", code)
            # 删除旧的验证码
            VerificationCode.objects.filter(user=user).delete()

            # 创建新的验证码
            VerificationCode.objects.create(user=user, code=code)

            # 发送邮件
            send_mail(
                '登录邮箱验证',
                f'您的验证码是: {code}，有效时间五分钟',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '邮箱未注册'})
    return JsonResponse({'status': 'error', 'message': '无效请求'})


def check_email_verification(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            return JsonResponse({
                'needs_verification': not user.email_verified and user.email
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({'needs_verification': False})
    return JsonResponse({'needs_verification': False})


def user_login(request):
    if request.method == 'POST':
        print('request.POST', request.POST)
        form = LoginForm(request.POST)
        print('form.is_valid', form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            verification_code = form.cleaned_data.get('verification_code', '')

            user = authenticate(username=username, password=password)
            print("user", user)

            if user is not None:
                if not user.email_verified and verification_code:
                    # 检查验证码
                    try:
                        vcode = VerificationCode.objects.get(
                            user=user,
                            code=verification_code,
                            created_at__gte=timezone.now() - timedelta(minutes=5)
                        )
                        user.email_verified = True
                        user.save()
                        vcode.delete()
                    except VerificationCode.DoesNotExist:
                        form.add_error('verification_code', '验证码错误或已过期')
                        return render(request, 'login.html', {'form': form})

                if user.email_verified or not user.email:
                    login(request, user)
                    # 设置会话为会话级别的会话
                    request.session.set_expiry(0)
                    return redirect('chat')
                else:
                    form.add_error(None, '请验证您的邮箱')
            else:
                form.add_error(None, '用户名或密码错误')
        else:
            # 打印表单错误信息
            print('表单验证错误:', form.errors)
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def chat(request):
    return render(request, 'django_qa.html')


from utils.nlp_processor import text_to_voice_llm


@csrf_exempt
def smart_query(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_query = data.get('query', '')
    print("user_query", user_query)

    #从session获取对话历史

    history = request.session.get('conversation_history', '')
    if not history:
        history = []

    persona_name = request.session.get('persona_name', '')
    persona_description = request.session.get('persona_description', '')
    print(persona_description)
    # 构建基础prompt
    base_prompt = persona_description + f'你的名字叫做:{persona_name}。回答控制在50字以内。'
    # 准备发送给大模型的消息列表
    messages = [{"role": "system", "content": base_prompt}]
    # 添加历史对话
    for item in history[-4:]:  # 只保留最近4轮对话
        messages.append({"role": "user", "content": item['user_query']})
        messages.append({"role": "assistant", "content": item['ai_response']})

    # 添加当前问题
    messages.append({"role": "user", "content": user_query})

    persona_voice = request.session.get('persona_voice','')
    style_map = {
        "standard_female": "zhijia",
        "gentle_female": "zhiyue",
        "loli_female": "zhiwei",
        "caring_female": "zhiyuan",
        "standard_male": "zhida",
        "humorous_male": "zhiming",
        "natural_male": "zhishuo",
        "magnetic_male": "zhixiang",
    }

    polished_text = polish_results_with_llm(messages)

    # 保存当前对话到历史
    history.append({
        'user_query': user_query,
        'ai_response': polished_text
    })
    request.session['conversation_history'] = history
    request.session.modified = True

    voice = text_to_voice_llm(style_map.get(persona_voice, 'zhijia'), polished_text)
    # print(voice)
    if voice is not None:
        # 构建保存音频文件的目录，结合 MEDIA_ROOT 和 'audio' 目录
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
        # 确保音频保存目录存在，如果不存在则创建
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        # 构建完整的文件名，包含唯一的 UUID
        file_name = os.path.join('audio', f"{uuid.uuid4()}.wav")
        # 保存文件到默认存储
        saved_path = default_storage.save(file_name, ContentFile(voice))
        # 返回包含音频URL的JSON
        return JsonResponse({
            'text': polished_text,
            'audio_url': default_storage.url(saved_path)
        })
    return HttpResponse(status=500)


def person_setting(request):
    return render(request, 'django_set_person.html')


def user_setting(request):
    return render(request, 'django_user_setting.html')


@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'avatar_url': user.get_avatar_url(),
        'nickname': user.nickname if user.nickname else '暂无昵称',
        'phone': user.phone if user.phone else '未绑定',
        'email': user.email if user.email else '未绑定',
        'signature': user.signature if user.signature else '暂无签名',
    }
    return render(request, 'django_user_setting.html', context)


@login_required
def update_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '头像更新成功')
        else:
            messages.error(request, '头像更新失败')
    return redirect('profile')


@login_required
def update_nickname(request):
    if request.method == 'POST':
        form = NicknameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '昵称更新成功')
        else:
            messages.error(request, '昵称更新失败')
    return redirect('profile')


@login_required
def update_phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '手机号更新成功')
        else:
            messages.error(request, '手机号更新失败')
    return redirect('profile')


@login_required
def update_email(request):
    user = request.user
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            # 验证邮箱
            verification_code = request.POST.get('verify_code')
            try:
                vcode = VerificationCode.objects.get(
                    user=user,
                    code=verification_code,
                    created_at__gte=timezone.now() - timedelta(minutes=5)
                )
                # 如果存在就把该记录删除
                vcode.delete()
            except VerificationCode.DoesNotExist:
                form.add_error('verification_code', '验证码错误或已过期')

            form.save()
            messages.success(request, '邮箱更新成功')
        else:
            messages.error(request, '邮箱更新失败')
    return redirect('profile')


@login_required
def update_signature(request):
    if request.method == 'POST':
        form = SignatureForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个性签名更新成功')
        else:
            messages.error(request, '个性签名更新失败')
    return redirect('profile')
