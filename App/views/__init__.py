# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .competition import competition_views
from .admin import setup_admin


views = [user_views, index_views, auth_views, competition_views] 
# blueprints must be added to this list