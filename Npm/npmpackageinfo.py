import requests, json, os
from .iputil import get_ip
from semantic_version import Spec, Version
import time

package_list = []
packagec_list = []
package = ""
packagec = ""


def registryresponse(name):
    response = requests.get("http://registry.npmjs.org/" + name + "/")
    binary = response.content
    output = json.loads(binary)
    return output


def getnpmpackagedependencies(name, version, request):
    output = registryresponse(name)
    version = versioncheck(output, version)
    if "/" in name:
        check = name.split("/")[1]
    else:
        check = name
    global packagec
    packagec = check+"-"+version
    packagec = packagec.strip()
    if 'dependencies' in output["versions"][version]:
        for key, value in output["versions"][version]['dependencies'].items():
            packaget = key + "-" + value
            packaget = packaget.strip()
            if "||" in value:
                value = value.split("||")[-1].strip()
            if packaget not in packagec_list:
                version = getpackagetarball(key, value, request)
                packagec_list.append(packaget)
                getnpmpackagedependencies(key, version, request)


def getpackagetarball(name, version, request):
    output = registryresponse(name)
    version = versioncheck(output, version)
    if "*" in version:
        if 'latest' in output:
            version = output["latest"]
        elif 'dist-tags' in output:
            version = output["dist-tags"]["latest"]
    url = output["versions"][version]['dist']['tarball']
    url = url.replace("https", "http").strip()
    global packagec
    if url not in package_list:
        downloadpackage(url, request)
        package_list.append(url)
        print("Package Downloaded: "+url)
    else:
        print("Package already downloaded: " + packagec)
    return version


def downloadpackage(url, request):
    filename = url.split("/")[-1]
    with open("download/"+get_ip(request)+"/"+filename, "wb") as f:
        r = requests.get(url)
        f.write(r.content)
    #time.sleep(1)


def versioncheck(output, version):
    if len(version) == 3:
        version = version.split(".")[0]
        version = get_npm_latest_version(output, version)
    if "^" in version or "~" in version or len(version) == 1 or "X" in version or "x" in version or ">=" in version:
        if "X" in version or "x" in version:
            version = version.split(".")[0]
        elif ">=" in version:
            if "<" in version:
                version = version.split(" ")[1]
        version = get_npm_latest_version(output, version)
    return version


def get_npm_latest_version(output, range):
    versions = map(str, output['versions'].keys())
    versions = map(Version, versions)
    range_spec = Spec(range)
    versions = range_spec.filter(versions)
    for v in versions:
        version = v
    return str(version)
