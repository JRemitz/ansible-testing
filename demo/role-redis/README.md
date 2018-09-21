role-redis
=========

This is an example role that does nothing more than prints a debug message. The "meat" is within the molecule tests for the purpose of the demonstration.

Requirements
------------

Testing requirements:

- `pip install molecule docker`
- System package: Docker

Role Variables
--------------

None

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in
regards to parameters that may need to be set for other roles, or variables that
are used from other roles.

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: redis }

Testing
------------

`molecule test --all`

License
-------

MIT

Author Information
------------------

Jake Remitz
