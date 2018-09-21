import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


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
