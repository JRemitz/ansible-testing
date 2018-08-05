### Enterprise role-play: Dress up your Ansible roles with great tests


Jake Remitz | Technical Team Lead | @jremitz

---

### **Question**: *Who’s testing their infrastructure and how?*

+++

## Testing Tools

@ul

- Serverspec (ruby-based - https://serverspec.org/
- Testinfra (python-based) - https://testinfra.readthedocs.io/en/latest/
- InSpec - https://www.inspec.io/
- Bats (Bash Automated Testing System) - https://github.com/sstephenson/bats
- GOSS (yaml-based) - https://goss.rocks

@ulend

+++

### Ansible-specific Testing

#### Syntax Check

```sh
ansible-playbook test_playbook.yml -i hosts --syntax-check
```

#### Check Play

```sh
ansible-playbook test_playbook.yml -i hosts --check
```

+++

## Testing Orchestrators

@ul

- KitchenCI (“test kitchen” – alternative to molecule) - https://kitchen.ci/
- Molecule - http://molecule.readthedocs.io/

@ulend

---

## Molecule

Orchestrate the end-to-end testing of your ansible roles including dependencies, infrastructure provisioning, and playbook execution.

+++

### Ansible tests

- lint
- syntax
- check
- provision
- idempotency

+++

[Molecule Usage](https://molecule.readthedocs.io/en/latest/usage.html)

```yml
hosts: test
tasks
  - name: test task
    debug:
      msg: "{{ output }}"
```