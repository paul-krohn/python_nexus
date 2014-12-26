import requests
import hashlib
from lxml import etree
import os


class Nexus(object):
    def __init__(self, nexus_base_url="", **kwargs):
        self.nexus_auth = False
        # check passed-in args, and env, for nexus user/pass, else leave blank
        if "user" in kwargs.keys() and "password" in kwargs.keys():
            self.nexus_auth = True
            self.nexus_user = kwargs["user"]
            self.nexus_pass = kwargs["password"]

        if nexus_base_url == "":
            raise ValueError("missing required argument nexus_base_url")
        else:
            self.nexus_base_url = nexus_base_url

        if "download_directory" in kwargs.keys():
            self.download_directory = kwargs["download_directory"]
        else:
            self.download_directory = os.getcwd()
        self.verbose = False
        if "verbose" in kwargs.keys():
            self.verbose = True

    @staticmethod
    def _hash_file(file_path):
        sha1 = hashlib.sha1()
        f = open(file_path, 'rb')
        try:
            sha1.update(f.read())
        finally:
            f.close()
        return sha1.hexdigest()

    def _resolver_url(self, group_id, artifact_id, version, repository, packaging):
        return self.nexus_base_url + "/service/local/artifact/maven/resolve" + \
            "?g=" + group_id + \
            "&a=" + artifact_id + \
            "&v=" + version + \
            "&r=" + repository + \
            "&p=" + packaging

    def _resolve_artifact(self, group_id, artifact_id, version, repository, packaging):
        resolver_url = self._resolver_url(group_id, artifact_id, version, repository, packaging)
        if self.nexus_auth:
            resolver_response = requests.get(resolver_url, auth=(self.nexus_user, self.nexus_pass))
        else:
            resolver_response = requests.get(resolver_url)
        if resolver_response.status_code != 200:
            raise ValueError("bad response (%s) for resolver URL %s" % (resolver_response.status_code, resolver_url))
        return resolver_response.content

    def _artifact_url(self, artifact_path, public=True):
        return "%s/content/groups/%s%s" % (self.nexus_base_url, 'public' if public else 'private', artifact_path)

    def get_artifact(self, group_id, artifact_id, version="trunk-SNAPSHOT",
                     repository="snapshots", packaging="war", public=True):
        artifact_xml = self._resolve_artifact(group_id, artifact_id, version, repository, packaging)
        parsed_xml = etree.fromstring(artifact_xml)

        artifact_path = parsed_xml.xpath("/artifact-resolution/data/repositoryPath")[0].text
        artifact_sha1 = parsed_xml.xpath("/artifact-resolution/data/sha1")[0].text

        print "artifact url is: %s" % self._artifact_url(artifact_path, public)

        # do we already have the file, with the requisite sha1 hash?
        local_artifact_path = os.path.join(self.download_directory, os.path.basename(artifact_path))
        if os.path.exists(local_artifact_path) and self._hash_file(local_artifact_path) == artifact_sha1:
            # we've already got the file, don't bother to download
            return True
        else:
            if self.nexus_auth:
                download_response = requests.get(self._artifact_url(artifact_path, public),
                                                 auth=(self.nexus_user, self.nexus_pass), stream=True)
            else:
                download_response = requests.get(self._artifact_url(artifact_path, public), stream=True)
            with open(local_artifact_path, 'wb') as f:
                for chunk in download_response.iter_content(chunk_size=4096):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
