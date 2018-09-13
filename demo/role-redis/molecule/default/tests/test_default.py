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
    assert host.run_expect([0], "redis-cli -p 6379 info")
