"""
URL configuration for execution_devops project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path, include, re_path
from evm_bff.views import ActiveTestCycleStatics, ActiveTestCaseDetails, ActiveTestCaseComplete, ActiveTestCaseStart, \
    ActiveTestCaseReStart, ActiveTestCaseAssign, UploaddbView
from evm_bff.views import StaticTestCycle
from evm_bff.views import ActiveTestCycle, ActiveTestCycleDetails, ActiveTestCycleStart, ActiveTestCycleStop, ActiveTestCaseStage
from evm_bff.views import ActiveTestExecution
from evm_bff.views import TestCaseResult
from evm_bff.views import Users

from evm_bff.views import Loginview

urlpatterns = [
    path('active-testcycle/',ActiveTestCycle.as_view(), name='active-testcycle'),
    path('testcycle/',StaticTestCycle.as_view(), name='testcycle-hsdes'),
    re_path('login/',Loginview.as_view(), name='login'),
    re_path('upload/',UploaddbView.as_view(), name='upload'),
    re_path('active-testcycle/(?P<cycle_id>\d+)/start/$',ActiveTestCycleStart.as_view()),
    re_path('active-testcycle/statics/$',ActiveTestCycleStatics.as_view()),
    re_path('active-testcycle/(?P<cycle_id>\d+)/stop/$',ActiveTestCycleStop.as_view()),
    re_path('active-testcycle/(?P<cycle_id>\d+)/$',ActiveTestCycleDetails.as_view()),
    re_path('active-testcycle/(?P<cycle_id>\d+)/assignment/$',ActiveTestCaseAssign.as_view(), name='active-testcase-list'),
    re_path('active-testcases/(?P<testcase_id>\d+)/$',ActiveTestCaseDetails.as_view(), name='active-testcase-list'),
    re_path('active-testcases/(?P<testcase_id>\d+)/stage/$',ActiveTestCaseStage.as_view(), name='active-testcase-list'),
    re_path('active-testcases/(?P<cycle_id>\d+)/(?P<testcase_id>\d+)/complete/$',ActiveTestCaseComplete.as_view(), name='active-testcase-list'),
    re_path('active-testcases/(?P<cycle_id>\d+)/(?P<testcase_id>\d+)/start/$',ActiveTestCaseStart.as_view(), name='active-testcase-list'),
    re_path('active-testcases/(?P<cycle_id>\d+)/(?P<testcase_id>\d+)/restart/$',ActiveTestCaseReStart.as_view(), name='active-testcase-list'),
    re_path('active-testcases/(?P<cycle_id>\d+)/(?P<testcase_id>\d+)/execution/$',ActiveTestExecution.as_view(), name='active-teststep-action'),
    re_path('userlogin/&',Loginview.as_view, name='login'),
    re_path('users/$',Users.as_view(), name='user'),
    re_path('testcase-result/',TestCaseResult.as_view(), name='testcase-result-sync'),
]
