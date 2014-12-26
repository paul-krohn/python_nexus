python-nexus
============

A nexus client in Python. Use it to add the ability to download jar, war or pom files from a nexus repo, typically before deploying to tomcat or another container.

See the included example_script.py for a sample usage.

First, import, initialize and configure the library (assuming it does not require authentication):
```python
>>> from nexus_client.nexus import Nexus
>>> client = Nexus("https://your.nexus.url/path")
```

There is only one exposed method, `get_artifact`. It takes arguments specifying the Nexus co-ordinates:

* group id
* artifact id
* version (defaults to `LATEST`)

As well as a couple other things:

* repository name (such as `snapshots`, `releases `or whatever your Nexus configuration is)
* public or private repository? (defaults to `public`, pass in public=False to use `private`
* packaging (defaults to `jar`)

So for example:
```python
client.get_artifact(
    group_id="org.apache.ant",
    artifact_id="ant",
    packaging="jar",
    version="LATEST",
    repository="releases")
```
Finally, sample usage of the example script:
```
./example_script.py -r releases -g org.apache.ant -a ant -v LATEST -s https://repository.apache.org
```
