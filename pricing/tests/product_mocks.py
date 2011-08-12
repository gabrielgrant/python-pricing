from mock import Mock

account = Mock(name='Account')
account.user.return_value = 'user'

get_storage_in_use = Mock(name='get_storage_in_use', return_value=2)

get_projects_in_use = Mock(name='get_projects_in_use', return_value=3)
