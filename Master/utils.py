#!/usr/bin/env python3
import docker
from docker import errors
import json
from io import BytesIO
from urllib import request


class Utils(object):
    def __init__(self, base_url):
        self.client = docker.DockerClient(base_url)

    def stop_containers(self, image_name):
        try:
            container_ids = self.client.containers.list(filters={'ancestor': image_name})
            for container_id in container_ids: container_id.remove(force=True)
            return True
        except docker.errors.APIError:
            return False

    def start_container(self, image_name, virtual_host):
        try:
            self.client.containers.run(image_name, detach=True, environment={'VIRTUAL_HOST': virtual_host})
            return True
        except (docker.errors.ContainerError, docker.errors.ImageNotFound, docker.errors.APIError):
            return False

    def search_container(self, image_name='jwilder/nginx-proxy'):
        # image_name = 'alpine:latest'
        try:
            self.client.images.get(image_name)
            return True
        except docker.errors.ImageNotFound:
            return False

    def check_status(self, image_name):
        if self.search_container(image_name):
            container_ids = self.get_container_ids(image_name)
            # when stopped and started there should be only one container in the container_ids list
            if len(container_ids) == 0:
                return 'STOPPED'
            else:
                if container_ids[0].status == 'running':
                    return 'RUNNING'
        else:
            return 'NOT AVAILABLE'

    def get_container_ids(self, image_name):
        return self.client.containers.list(filters={'ancestor': image_name})

    def start_nginx(self, image_name='jwilder/nginx-proxy:0.4.0'):
        try:
            if self.check_status(image_name) != 'RUNNING':
                self.client.containers.run(image_name, detach=True,
                                           volumes={'/var/run/docker.sock': {'bind': '/tmp/docker.sock', 'mode': 'ro'}},
                                           ports={'80/tcp': 8764})
            return True
        except (docker.errors.ContainerError, docker.errors.ImageNotFound, docker.errors.APIError):
            return False


class AdvancedUtils(object):
    def __init__(self, base_url):
        self.client = docker.APIClient(base_url)

    def pull_container_from_hub(self, image_name):
        try:
            if self.client.ping():
                for line in self.client.pull(image_name, stream=True):
                    j_line = json.loads(line.decode('utf-8'))
                    if j_line['status'] == 'Downloading':
                        j_progress_details = j_line['progressDetail']
                        progress_val = j_progress_details['current'] * 100 / j_progress_details['total']
                        # print(progress_val)
                        # print(j_line['progress'])
                        yield progress_val
                yield True
            else:
                yield False
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            yield False

    def build_container_from_url(self, url_path, tag):
        try:
            response = request.urlopen(url_path)
            data = BytesIO(response.read())
            for line in self.client.build(fileobj=data, rm=True, tag=tag):
                output = json.loads(line.decode('utf-8'))['stream']
                print(output)
                yield output
            yield True
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            yield False
