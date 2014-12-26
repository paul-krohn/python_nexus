#!/usr/bin/env python


from optparse import OptionParser

args_options = OptionParser()

args_options.add_option("-g", "--group-id", dest="groupid", help="group id")
args_options.add_option("-a", "--artifact-id", dest="artifactid", help="artifact id")
args_options.add_option("-v", "--version", dest="version", help="version of artifact", default="LATEST")
args_options.add_option("-r", "--repository", dest="repository", help="Nexus repository name", default="snapshots")
args_options.add_option("-p", "--packaging", dest="packaging", help="packaging (jar, war, etc.)", default="jar")
args_options.add_option("-s", "--nexus-url", dest="server",
                        help="nexus server", default="http://repository.sonatype.org")
args_options.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debugging", default=False)
args_options.add_option("-u", "--user", dest="user", help="username", default="")
args_options.add_option("--password", dest="password", help="HTTP Basic password", default="")

(options, args) = args_options.parse_args()

# an example is worth a thousand words
from nexus_client.nexus import Nexus
if options.user != "" and options.password != "":
    client = Nexus(options.server, user=options.user, password=options.password, verbose=True)
else:
    client = Nexus(options.server)
client.get_artifact(
    group_id=options.groupid,
    artifact_id=options.artifactid,
    packaging=options.packaging,
    version=options.version,
    repository=options.repository)