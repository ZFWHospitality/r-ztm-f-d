from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def swagger_bearer(request, *args, **kwargs):
    response = schema_view.with_ui('swagger', cache_timeout=0)(request, *args, **kwargs)
    response.render()

    if hasattr(response, 'content') and b'</body>' in response.content:
        html = response.content.decode()
        html = html.replace(
            "</body>",
            """
            <script>
            window.onload = function() {
              if (window.ui) {
                window.ui.getConfigs().requestInterceptor = function(req) {
                  if (req.headers['Authorization'] &&
                      !req.headers['Authorization'].startsWith('Bearer ')) {
                    req.headers['Authorization'] = 'Bearer ' + req.headers['Authorization'];
                  }
                  return req;
                };
              }
            };
            </script>
            </body>
            """
        )
        response.content = html.encode()

    return response