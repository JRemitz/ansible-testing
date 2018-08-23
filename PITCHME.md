@size[40pt](@color[#FF694B](**Enterprise role-play**)@color[#333F48](: Dress up your Ansible roles with great tests))

@snap[south]
@size[18pt](Jake Remitz | Technical Team Lead) <br />
@size[14pt](@fa[github] @fa[twitter-square] @jremitz)
@snapend

---

@fa[question-circle fa-3x]
### Who’s testing their infrastructure and how?

+++
### Ansible Core on Testing...

[Ansible Testing Strategies](https://docs.ansible.com/ansible/latest/test_strategies.html)

> @size[22pt](Ansible believes you should not need another framework to validate basic things of your infrastructure is true. This is the case because Ansible is an order-based system that will fail immediately on unhandled errors for a host, and prevent further configuration of that host. This forces errors to the top and shows them in a summary at the end of the Ansible run.)

+++

### Ansible-specific Testing
<br /> 
##### Syntax Check
 
```sh
ansible-playbook test_playbook.yml -i hosts --syntax-check
```

@css[page-note](Not much of a "test" - but it's a good sanity check to start)

+++
##### Check Play

```sh
ansible-playbook test_playbook.yml -i hosts --check
```

@css[page-note](Good dry run but may fail for some downstream tasks with dependencies - package install, for example)

+++

##### Helpful Features

**Modules**

- `wait_for`
- `uri`
- `stat`
- `fail (when)`
- `assert (that)`


@css[page-note](Will require "test" environment where impactful changes can be applied)

+++

**Loops**
- Do-Until

```yml
- shell: /usr/bin/foo
  register: result
  until: result.stdout.find("all systems go") != -1
  retries: 5
  delay: 10
```

+++?code=src/ansible/elk.yml&title=Elasticsearch Example Health Check

---

## Testing Tools

@ul

- Bats (Bash Automated Testing System) - https://github.com/sstephenson/bats
- Serverspec - https://serverspec.org/
- GOSS - https://goss.rocks
- InSpec - https://www.inspec.io/
- Testinfra - https://testinfra.readthedocs.io/en/latest/

@ulend

+++

## Testing Orchestrators

- KitchenCI (“Test Kitchen”) - https://kitchen.ci/
- Molecule - http://molecule.readthedocs.io/

<br />

#### Benefits

- Pre-built flow of common testing techniques (provision, test, decommission)

---

## Molecule

> Orchestrate the end-to-end testing of your ansible roles including dependencies, infrastructure provisioning, and playbook execution.

@css[page-note](Supports: Azure, Docker, EC2, GCE, LXC, LXD, Openstack, Vagrant, and others)
+++

### Uses

- lint
- syntax
- dependencies (galaxy, gilt, shell)
- check
- provision
- idempotency
- verify

[Molecule Usage](https://molecule.readthedocs.io/en/latest/usage.html)

+++

### Demo

Note:

- `molecule help`
- **Greenfield**: `molecule init role -r test-role -d docker --lint-name yamllint --verifier-name testinfra`
- **Brownfield**: `molecule init scenario -r test-role -d docker --lint-name yamllint --verifier-name testinfra`
