Server=AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/Node:' + AdminControl.getNode() + '/Server:server1')
Node=AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/Node:' + AdminControl.getNode() + '/')
Cell=AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/')
NodeName=AdminControl.getNode()

VH=AdminConfig.getid('/VirtualHost:default_host/')
AdminConfig.create('HostAlias', VH, '[[hostname "*"][port "9044"]]')
AdminConfig.create('HostAlias', VH, '[[hostname "*"][port "19443"]]')
AdminConfig.create('HostAlias', VH, '[[hostname "*"][port "19444"]]')
AdminConfig.create('HostAlias', VH, '[[hostname "*"][port "19080"]]')
AdminConfig.create('HostAlias', VH, '[[hostname "*"][port "19081"]]')

AdminConfig.save()
