# Demo - Redis

## New Scenario - Default installation

1. Create empty role with defaults (yamllint, Docker, testinfra)
    
    `molecule init role -r role-redis`
1. `molecule.yml` - Swap containers for **systemd** containers
    ```
    platforms:
    - name: instance1
        image: jremitz/centos-systemd:latest
        privileged: true
        command: /usr/sbin/init
    ```
1. Create the platforms
    `molecule create`
1. Make our new redis role do *something* by adding a debug command in the tasks: `tasks/main.yml`
    ```yml
    ---
    - name: Demo output
      debug: msg="Redis role has run"
    ```
1. Test Driven Development (TDD) - Let's add some tests so it fails!
    [Testinfra - host fixture](https://testinfra.readthedocs.io/en/latest/modules.html#host)
    `molecule/default/tests/test_default.py`
    ```py
    def test_redis(host):
        assert host.package("redis").is_installed
        assert host.process.get(user="redis", comm="redis-server")
        assert host.run_expect([0], "redis-cli -p 6379 info")
    ```
1.  `requirements.yml` - Add dependencies, where we're getting the code
    ```
    ---
    - src: geerlingguy.repo-epel
      name: epel
    - src: git+https://github.com/JRemitz/ansible-role-redis
      version: slave-master
      name: ansible-role-redis
      
    ```
1. Watch your tests fail (TDD) by converging and verifying the results

    `molecule converge`

    and now verify
    
    `molecule verify`

    You should have failed verify results with an AssertionError

    ```sh
    =================================== FAILURES ===================================
    ________________________ test_redis[ansible://instance] ________________________

    host = <testinfra.host.Host object at 0x7f659ee45350>

        def test_redis(host):
    >       assert host.package("redis").is_installed
    E       AssertionError: assert False
    E        +  where False = <package redis>.is_installed
    E        +    where <package redis> = <class 'testinfra.modules.base.RpmPackage'>('redis')
    E        +      where <class 'testinfra.modules.base.RpmPackage'> = <testinfra.host.Host object at 0x7f659ee45350>.package

    tests/test_default.py:18: AssertionError
    ===================== 1 failed, 1 passed in 13.47 seconds ======================
    ```
1. To fix this, let's now install epel, redis, and then re-verify by updating the `playbook.yml` and adding *epel* and *ansible-role-redis* roles

    ```yml
    ---
    - name: Converge
      hosts: all
      roles:
        - role: epel
        - role: ansible-role-redis
        - role: redis

    ```

1. Re-run converge

    `molecule converge`

    and verify

    `molecule verify`

    ```sh
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.5, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
    rootdir: /vagrant_data/ansible-testing/demo/tmp/redis/molecule/default, inifile:
    plugins: testinfra-1.14.1
    collected 2 items

    tests/test_default.py ..                                                 [100%]

    ========================== 2 passed in 16.95 seconds ===========================
    ```

## New Scenario - Test Replication

1. Create a `replication` scenario for the same role to test redis replication

    `molecule init scenario -r role-redis -s replication`

1. Move the default role's playbook up a level so it can be shared across scenarios and modify both scenario's `molecule.yml` and copy to the new **replication** scenario
[Molecule - coniguration](https://molecule.readthedocs.io/en/latest/configuration.html)
    
    ```yml
    provisioner:
      name: ansible
      playbooks:
        converge: ../playbook.yml
    ```
    **NOTE** - You will need to update the scenario name in the slave's `molecule.yml` if you copy from the default scenario

1. Update the `molecule.yml` for a master/slave relationship between the docker containers
    1. Expose ports: `6379` (master), `6380` (slave)
    1. Add second instance for slave
    1. Add master/slave child groups

        ```yml
        platforms:
        - name: instance1-master
            image: jremitz/centos-systemd:latest
            privileged: true
            command: /usr/sbin/init
            groups:
            - redis
            children:
            - redis_master
            exposed_ports:
            - 6379/tcp
            published_ports:
            - 0.0.0.0:6379:6379/tcp
        - name: instance2-slave
            image: jremitz/centos-systemd:latest
            privileged: true
            command: /usr/sbin/init
            groups:
            - redis
            children:
            - redis_slave
            exposed_ports:
            - 6380/tcp
            published_ports:
            - 0.0.0.0:6380:6380/tcp
        ```
    1. Add Ansible group vars for IP, port, and password

        ```yml
        provisioner:
        name: ansible
        playbooks:
            converge: ../playbook.yml
        inventory:
            group_vars:
            redis:
                redis_bind_interface: 0.0.0.0
                redis_requirepass: secret
            redis_slave:
                redis_port: 6380
                redis_slaveof: "{{ groups['redis_master'] | map('extract', hostvars, ['ansible_eth0','ipv4','address']) | first }} 6379"
        ```

1. After running `converge`

    `molecule converge`

    test the "external" connection outside of docker

    `redis-cli -a secret info replication`

1. Test linter in `molecule.yml`, *flake8* - override options to allow longer lines if you run into issues linting your test cases
    ```yml
    verifier:
      name: testinfra
      lint:
        name: flake8
        options:
          max-line-length: 100
    ```

1. Update the test so that slave is connected and services are running

    ```py
    def test_redis(host):
        assert host.package("redis").is_installed
        assert host.process.get(user="redis", comm="redis-server")
        vars = host.ansible.get_variables()
        if "redis_port" in vars:
            assert host.run_expect(
                [0], "redis-cli -p %s info" % vars["redis_port"])


    def test_redis_replication(host):
        vars = host.ansible.get_variables()
        if "redis_master" in vars["group_names"]:
            # Validate master replication
            result = host.run("redis-cli -a %s info replication" % vars["redis_requirepass"])
            assert "connected_slaves:1" in result.stdout
        else:
            # Validate slave replication
            result = host.run("redis-cli -a %s -p 6380 info replication" % vars["redis_requirepass"])
            assert "master_link_status:up" in result.stdout
    ```

1. After verifying that everything tests successfully

    `molecule verify`

    Ensure that everything works together by running end-to-end and validating all test cases/scenarios

    `molecule test --all`