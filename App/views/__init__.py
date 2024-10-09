# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .competition_view import competitions_view
from .admin import setup_admin


views = [user_views, index_views, auth_views, competitions_view] 
# blueprints must be added to this list