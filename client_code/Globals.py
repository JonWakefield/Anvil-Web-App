import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

# Global VAR USED TO STORE USER INFO: Type: Dict
# users = {
#   'username': str
#   'email': str
#   'active_gin': str
#   'role': str
#   'gins_accessible': list[str]
#   'num_gin_stands': list[int]
#   'gin_location': list[str]
# }
user = None

# Role permissions mapping: Implement Role-Based Access Control (RBAC).
# Map roles to accessible webpage URLs. Improves client-side security. 
role_permissions = {
  'Admin': ['', 
            'camera-controls', 
            'node-connections',
            'picture-capture-controls',
            'gin-monitor',
            'graph-setup',
            'graph-viewer',
            'settings'],
  'Coordinator': ['',
                  'gin-monitor',
                  'graph-setup',
                  'graph-viewer',
                  'settings'],
  'Geo-Coordinator':['',
                     'gin-monitor',
                     'graph-setup',
                     'graph-viewer',
                     'settings'],
  'Manager':['',
             'gin-monitor',
             'graph-setup',
             'graph-viewer',
             'settings'],
  'Technician':['',
                'node-connections'
                'settings']
}


def check_user_form_privleges(url_hash, user_permissions):
  """"""
  if url_hash not in user_permissions:
    return False
  return True
  