"""driveinn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from DriveInnapp import views

urlpatterns = [
    path('', views.login),
    path('login_post', views.login_post),
    path('admin_home', views.admin_home),
    path('admin_index', views.admin_index),
    path('view_user', views.view_user),
    path('view_feedback', views.view_feedback) ,
    path('view_verify_workers', views.view_verify_workers),
    path('view_verified_workers', views.view_verified_workers),
    path('view_complaints', views.view_complaints),
    path('reply/<id>', views.reply),
    path('reply_sent/<id>', views.reply_sent),
    path('change_password', views.change_password),
    path('change_password_post', views.change_password_post),
    path('approve_worker/<id>', views.approve_worker),
    path('reject_worker/<id>', views.reject_worker),
    path('view_rating_review/<id>', views.view_rating_review),
    path('logout', views.logout),
    path('register', views.register),
    path('register_post', views.register_post),
    path('secret_code', views.secret_code),
    path('profile_update', views.profile_update),
    path('profile_update_post', views.profile_update_post),
    path('view_request_verify', views.view_request_verify),
    path('approve_request/<id>', views.approve_request),
    path('reject_request/<id>', views.reject_request),
    path('view_verified_request', views.view_verified_request),
    path('work_complete/<id>', views.work_complete),
    path('view_work_history', views.view_work_history),
    path('view_work_history_date', views.view_work_history_date),
    path('send_wcomplaints', views.send_wcomplaints),
    path('send_wcomplaints_post', views.send_wcomplaints_post),
    path('view_wcomplaints', views.view_wcomplaints),
    path('view_wpayhistory', views.view_wpayhistory),
    path('view_wrating', views.view_wrating),
    path('worker_index', views.worker_index),
    path('change_pass', views.change_pass),
    path('change_pass_post', views.change_pass_post),
    path('chatt/<u>', views.chatt),
    path('chatsnd/<u>', views.chatsnd),
    path('chatrply', views.chatrply),
    path('forgot_password', views.forgot_password),
    path('forgot_password_post', views.forgot_password_post),
    # path('worker_view_credit_point',views.worker_view_credit_point),
    # path('worker_credit_convert/<cid>',views.worker_credit_convert),
    # path('ajax_view_credit_points',views.ajax_view_credit_points),
    # path('view_wpayhistory_post',views.view_wpayhistory_post),

#................................................................................................ ANDROID

    path('android_login', views.android_login),
    path('android_register', views.android_register),
    path('android_view_worker', views.android_view_worker),
    path('android_send_request', views.android_send_request),
    path('android_view_request_status', views.android_view_request_status),
    path('android_rental_service', views.android_rental_service),
    path('android_request_history', views.android_request_history),
    path('android_send_rating', views.android_send_rating),
    path('android_view_rating', views.android_view_rating),
    path('android_send_feedback', views.android_send_feedback),
    path('android_send_complaint', views.android_send_complaint),
    path('android_view_reply', views.android_view_reply),
    # path('android_view_payment_history', views.android_view_payment_history),
    # path('android_credit_points', views.android_credit_points),
    path('android_change_password', views.android_change_password),
    path('android_add_chat', views.android_add_chat),
    path('android_view_chat', views.android_view_chat),
    path('and_offline_payment', views.and_offline_payment),
    path('android_online_payment', views.android_online_payment),
    path('android_view_payment_history', views.android_view_payment_history),

#............................................................................Credit point

    path('mode',views.mode),
    path('payment',views.payment),
    path('and_ajax_view_credit_points',views.and_ajax_view_credit_points),
    path('android_credit_point_payment',views.android_credit_point_payment),











]



