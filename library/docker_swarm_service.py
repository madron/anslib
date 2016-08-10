#!/usr/bin/python

DOCUMENTATION = '''

module: docker_swarm_service

short_description: Manages docker swarm services.

version_added: "2.2"

author:
  - "Massimiliano Ravelli (massimiliano.ravelli@gmail.com)"

description:
  - Manage docker swarm services.
  - Requires docker >= 1.12 and docker-py >= 1.9
  - Supports check mode.

options:
  name:
      description:
        - Name of the service.
      type: str
      required: true
  image:
      description:
        - Docker image. Required when C(state) is I(present).
      type: str
      default: null
      required: false
  state:
      description:
        - Desired state of the service: I(present) or I(absent).
      choices:
        - absent
        - present
      default: present
      type: str
      required: false
  replicas:
      description:
        - Number of tasks.
      type: int
      required: false

extends_documentation_fragment:
    - docker

requirements:
    - "python >= 2.6"
    - "docker-py >= 1.9"
    - "Docker API >= 1.24"
'''

EXAMPLES = '''
- name: Create service
  docker_swarm_service:
    name: nginx
    image: nginx:alpine

- name: Scale service
  docker_swarm_service:
    name: nginx
    image: nginx:alpine
    replicas: 2

- name: Remove service
  docker_swarm_service:
    name: nginx
    state: absent
'''

RETURN = '''
ansible_docker_swarm_service:
    description:
      - Facts representing the current state of the service. Matches the docker inspection output.
      - Empty if C(state) is I(absent)
    returned: always
    type: dict
    sample: '{
    }
'''

from copy import deepcopy
from ansible.module_utils.basic import *
from ansible.module_utils.docker_common import *
from docker import utils
from docker.errors import NotFound


AUTH_PARAM_MAPPING = {
    u'docker_host': u'--host',
    u'tls': u'--tls',
    u'cacert_path': u'--tlscacert',
    u'cert_path': u'--tlscert',
    u'key_path': u'--tlskey',
    u'tls_verify': u'--tlsverify'
}
SERVICE_PARAMETERS = dict(
    name=dict(type='str', required=True),
    image=dict(type='str'),
    arg=dict(type='list', default=[]),
    mode=dict(type='str', choices=['replicated', 'global'], default='replicated'),
    replicas=dict(type='int', default=1),
)
ARGUMENT_SPEC = deepcopy(SERVICE_PARAMETERS)
ARGUMENT_SPEC['state'] = dict(type='str', choices=['absent', 'present'], default='present')


class ServiceApiMixin(object):
    @utils.minimum_version('1.22')
    def services(self, filters=None):
        params = {
            'filters': utils.convert_filters(filters) if filters else None
        }
        url = self._url('/services')
        return self._result(self._get(url, params=params), True)

    def get_service_data(self, **kwargs):
        '''
        arg                     Service command args (default [])
        command                 Service command (default [])
        constraint              Placement constraints (default [])
        endpoint_mode           Endpoint mode(Valid values: VIP, DNSRR)
        env                     Set environment variables (default [])
        image                   Service image tag
        label                   Service labels (default [])
        limit_cpu               Limit CPUs (default 0.000)
        limit_memory            Limit Memory (default 0 B)
        mode                    Service mode (replicated or global)
                                (default "replicated")
        mount                   Attach a mount to the service
        name                    Service name
        network                 Network attachments (default [])
        publish                 Publish a port as a node port (default [])
        replicas                Number of tasks (default none)
        reserve_cpu             Reserve CPUs (default 0.000)
        reserve_memory          Reserve Memory (default 0 B)
        restart_condition       Restart when condition is met
                                (none, on_failure, or any)
        restart_delay           Delay between restart attempts (default none)
        restart_max_attempts    Maximum number of restarts before
                                giving up (default none)
        restart_window          Window used to evalulate the restart
                                policy (default none)
        stop_grace_period       Time to wait before force killing a
                                container (default none)
        update_delay            Delay between updates
        update_parallelism      Maximum number of tasks updated simultaneously
        user                    Username or UID
        workdir                 Working directory inside the container
        '''
        image = kwargs['image']
        data = {}
        if 'name' in kwargs:
            data['Name'] = kwargs['name']
        # TaskTemplate
        data['TaskTemplate'] = {
            "ContainerSpec": {
                "Image": image,
                "Args": kwargs.get('arg', []),
            },
            "Resources": {
                "Limits": {},
                "Reservations": {}
            },
            "RestartPolicy": {
                "Condition": "any",
                "MaxAttempts": 0
            },
            "Placement": {}
        }
        # Mode
        mode = kwargs.get('mode', 'replicated')
        if mode == 'global':
            data['Mode'] = {'Global': {}}
        if mode == 'replicated':
            data['Mode'] = {
                'Replicated': {'Replicas': kwargs.get('replicas', 1)}
            }
        # UpdateConfig
        # data['UpdateConfig'] = {
        #     "Parallelism": 1
        # },
        # EndpointSpec
        data['EndpointSpec'] = {
            "Mode": "vip"
        }
        return data

    @utils.minimum_version('1.22')
    def create_service(self, **kwargs):
        url = self._url('/services/create')
        data = self.get_service_data(**kwargs)
        return self._result(self._post_json(url, data=data), True)

    @utils.minimum_version('1.22')
    def update_service(self, service_id, version, **kwargs):
        url = self._url('/services/{0}/update', service_id)
        data = self.get_service_data(**kwargs)
        res = self._post_json(url, data=data, params={'version': version})
        self._raise_for_status(res)

    @utils.minimum_version('1.22')
    def inspect_service(self, name):
        url = self._url('/services/{0}', name)
        return self._result(self._get(url), True)

    @utils.minimum_version('1.22')
    def remove_service(self, name):
        url = self._url('/services/{0}', name)
        resp = self._delete(url)
        self._raise_for_status(resp)


class AnsibleDockerClientExtended(AnsibleDockerClient, ServiceApiMixin):
    pass


class SwarmServiceManager(DockerBaseClass):
    def __init__(self, client):
        super(SwarmServiceManager, self).__init__()
        self.client = client
        self.state = None
        self.parameters = self.client.module.params
        self.check_mode = self.client.check_mode

        self.name = self.parameters.get('name')

        self.result = dict(
            changed=False,
            actions=dict(),
        )

        for key, value in client.module.params.items():
            setattr(self, key, value)

        self.check_mode = client.check_mode

        if not self.debug:
            self.debug = client.module._debug

        self.options = dict()
        self.options.update(self._get_auth_options())

        self.log("options: ")
        self.log(self.options, pretty_print=True)

    def exec_module(self):
        result = dict()

        if self.state == 'present':
            self.present()
        elif self.state == 'absent':
            self.absent()

        if not self.check_mode and not self.debug and result.get('actions'):
            self.result.pop('actions')

        return self.result

    def _get_auth_options(self):
        options = dict()
        for key, value in self.client.auth_params.items():
            if value is not None:
                option = AUTH_PARAM_MAPPING.get(key)
                if option:
                    options[option] = value
        return options

    def get_wanted_service_params(self):
        params = dict()
        for key in SERVICE_PARAMETERS.keys():
            params[key] = self.parameters[key]
        return params

    def get_service(self):
        try:
            return self.client.inspect_service(self.name)
        except NotFound:
            return None

    def get_current_service_params(self, service):
        params = dict()
        params['name'] = service['Spec']['Name']
        params['image'] = service['Spec']['TaskTemplate']['ContainerSpec']['Image']
        params['arg'] = service['Spec']['TaskTemplate']['ContainerSpec'].get('Args', [])
        mode = service['Spec']['Mode'].keys()[0]
        if mode == 'Replicated':
            params['mode'] = 'replicated'
            params['replicas'] = int(service['Spec']['Mode']['Replicated']['Replicas'])
        if mode == 'Global':
            params['mode'] = 'global'
            params['replicas'] = 1
        return params

    def present(self):
        wanted = self.get_wanted_service_params()
        # self.result['wanted'] = wanted
        service = self.get_service()
        if not service:
            # Create
            if not self.check_mode:
                self.result['changed'] = True
                return self.client.create_service(**wanted)
            return
        # self.result['service'] = service
        current = self.get_current_service_params(service)
        # self.result['current'] = current
        if not current == wanted:
            # Update
            service_id = service['ID']
            version = service['Version']['Index']
            if not self.check_mode:
                self.client.update_service(service_id, version, **wanted)
                self.result['changed'] = True

    def absent(self):
        service = self.get_service()
        params = self.get_wanted_service_params()
        if service:
            if not self.check_mode:
                self.client.remove_service(params['name'])
                self.result['changed'] = True


def main():
    client = AnsibleDockerClientExtended(
        argument_spec=ARGUMENT_SPEC,
        supports_check_mode=True
    )

    result = SwarmServiceManager(client).exec_module()
    client.module.exit_json(**result)


if __name__ == '__main__':
    main()
