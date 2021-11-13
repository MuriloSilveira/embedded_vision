from django.urls import path
from .views import index, configuracao, m_calibracao, r_calibracao, f_calibracao, video, liga, desliga, calib_video, prox_calib, result_calib, result_q_dia, result_q_lote, result_query

urlpatterns = [
    path('', index, name='index'),
    path('config', configuracao, name='configuracao'),
    path('m-calib', m_calibracao, name='m_calibracao'),
    path('calib', r_calibracao, name='r_calibracao'),
    path('f-calib', f_calibracao, name='f_calibracao'),
    path('result-calib', result_calib, name='result_calib'),
    path('result-dia', result_q_dia, name='result_q_dia'),
    path('result-lote', result_q_lote, name='result_q_lote'),
    path('result-query', result_query, name='result_query'),
    path('desliga', desliga, name='desliga'),
    path('video', video, name='video'),
    path('calib_video', calib_video, name='calib_video'),
    path('prox_calib', prox_calib, name='prox_calib'),
    path('liga', liga, name='liga'),
    path('desliga', desliga, name='desliga'),
]
