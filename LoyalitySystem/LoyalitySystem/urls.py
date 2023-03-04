
from django.contrib import admin
from django.urls import path, include
from polls.views import index_page, remote_cards_page, generate_cards_page, cards_info
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index'),
    path('remote/', remote_cards_page, name='remote_cards'),
    path('generate/', generate_cards_page, name='generate_cards'),
    path('cards_info/<int:cards_id>/', cards_info, name='cards_info')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns

